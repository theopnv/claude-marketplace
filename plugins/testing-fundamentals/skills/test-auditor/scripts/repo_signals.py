#!/usr/bin/env python3
"""Collect read-only test signals from a repository, as leads for a test audit.

Usage: python3 repo_signals.py <repo-path> [--since "12 months ago"] [--json]
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from fnmatch import fnmatch
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist", "build",
    "target", ".tox", ".nox", ".mypy_cache", ".pytest_cache", ".ruff_cache", "vendor",
    ".next", ".nuxt", "coverage", "htmlcov", "site-packages", ".idea", ".vscode",
    ".gradle", ".terraform", "bin", "obj", ".eggs",
}

LANGUAGES = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".jsx": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".kt": "Kotlin", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".swift": "Swift", ".c": "C", ".h": "C", ".cpp": "C++",
    ".hpp": "C++", ".cc": "C++", ".scala": "Scala", ".dart": "Dart", ".ex": "Elixir",
    ".exs": "Elixir",
}

TEST_NAME_PATTERNS = [
    "test_*.py", "*_test.py", "*_test.go", "*.test.js", "*.test.ts", "*.test.jsx",
    "*.test.tsx", "*.test.mjs", "*.spec.js", "*.spec.ts", "*.spec.jsx", "*.spec.tsx",
    "*Test.java", "*Tests.java", "*IT.java", "*Test.kt", "*Tests.kt", "*_spec.rb",
    "*_test.rb", "*Tests.cs", "*Test.cs", "*Test.php", "*_test.exs", "*_test.dart",
]
TEST_DIR_NAMES = {"test", "tests", "__tests__", "spec", "specs", "e2e", "integration_tests", "testing"}

CONFIG_GROUPS = {
    "Test configuration": [
        "pytest.ini", "tox.ini", "noxfile.py", "conftest.py", "jest.config.*", "vitest.config.*",
        "karma.conf.*", "playwright.config.*", "cypress.config.*", "cypress.json", ".mocharc*",
        "phpunit.xml*", "behave.ini",
    ],
    "Coverage configuration": [".coveragerc", ".nycrc*", "codecov.yml", ".codecov.yml", "jacoco*.xml"],
    "CI pipelines": [
        ".github/workflows/*.yml", ".github/workflows/*.yaml", ".gitlab-ci.yml", "Jenkinsfile",
        "azure-pipelines.yml", ".circleci/config.yml", "bitbucket-pipelines.yml", ".travis.yml",
        ".buildkite/*",
    ],
    "Static analysis": [
        "ruff.toml", ".ruff.toml", "mypy.ini", ".flake8", ".pylintrc", "pylintrc", ".eslintrc*",
        "eslint.config.*", "biome.json", "tsconfig.json", ".golangci.y*ml", "clippy.toml",
        ".rubocop.yml", "sonar-project.properties", ".semgrep.y*ml", "checkstyle*.xml",
        ".pre-commit-config.yaml", "pyrightconfig.json",
    ],
    "Review and defect templates": [
        ".github/pull_request_template.md", ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/PULL_REQUEST_TEMPLATE/*", "CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS",
        ".github/ISSUE_TEMPLATE/*", ".gitlab/merge_request_templates/*", ".gitlab/issue_templates/*",
    ],
    "Environment and dependency control": [
        "Dockerfile", "*.Dockerfile", "docker-compose*.y*ml", "compose.y*ml", "poetry.lock", "uv.lock",
        "Pipfile.lock", "requirements*.txt", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "go.sum", "Cargo.lock", "Gemfile.lock", "composer.lock", ".tool-versions", ".python-version",
        ".nvmrc", "devcontainer.json", ".devcontainer/*",
    ],
    "Test basis candidates": [
        "README*", "SPEC*", "REQUIREMENTS*", "CHANGELOG*", "*.feature", "docs/*.md", "adr/*",
        "docs/adr/*", "user-stories/*", "stories/*",
    ],
}

PYPROJECT_SECTIONS = {
    "[tool.pytest": "Test configuration",
    "[tool.coverage": "Coverage configuration",
    "[tool.ruff": "Static analysis",
    "[tool.mypy": "Static analysis",
    "[tool.pylint": "Static analysis",
    "[tool.pyright": "Static analysis",
}

SKIP_PATTERNS = [
    r"@pytest\.mark\.skip", r"@pytest\.mark\.xfail", r"@unittest\.skip", r"pytest\.skip\(",
    r"\b(it|test|describe)\.(skip|todo)\(", r"\bx(it|describe)\(", r"\bt\.Skip\(",
    r"@Disabled\b", r"@Ignore\b", r"#\[ignore\]",
]
JS_TEST_CALL = re.compile(r"\b(it|test)\s*\(")
JS_ASSERT = re.compile(r"\b(expect|assert)\w*\s*[\.(]|\.should\b|\bt\.(is|deepEqual|true|false|throws)\(")

FIX_GREP = r"fix|bug|defect|hotfix|regression|patch|issue|broken|error"


def is_test_file(rel: Path) -> bool:
    name = rel.name
    if any(fnmatch(name, p) for p in TEST_NAME_PATTERNS):
        return True
    return any(part.lower() in TEST_DIR_NAMES for part in rel.parts[:-1])


def walk(repo: Path, max_files: int):
    count = 0
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.endswith(".egg-info")]
        for f in files:
            count += 1
            if count > max_files:
                return
            yield Path(root, f).relative_to(repo)


def count_lines(path: Path) -> int:
    try:
        with open(path, "rb") as fh:
            return sum(1 for line in fh if line.strip())
    except OSError:
        return 0


def python_tests_without_assert(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except (SyntaxError, ValueError):
        return []
    missing = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test"):
            if not _has_python_check(node):
                missing.append(f"{node.name} (line {node.lineno})")
    return missing


def _has_python_check(func: ast.AST) -> bool:
    for sub in ast.walk(func):
        if isinstance(sub, ast.Assert):
            return True
        if isinstance(sub, ast.Call):
            target = sub.func
            name = target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
            lowered = name.lower()
            if lowered.startswith("assert") or lowered in {"raises", "fail", "expect", "approx", "warns"}:
                return True
            if lowered.startswith("expect") or lowered.startswith("check") or lowered.startswith("verify"):
                return True
    return False


def js_tests_without_assert(text: str) -> bool:
    return bool(JS_TEST_CALL.search(text)) and not JS_ASSERT.search(text)


def find_configs(repo: Path, files: list[Path]) -> dict[str, list[str]]:
    found: dict[str, set[str]] = defaultdict(set)
    rel_strings = [str(f).replace(os.sep, "/") for f in files]
    for group, patterns in CONFIG_GROUPS.items():
        for rel in rel_strings:
            name = rel.rsplit("/", 1)[-1]
            depth = rel.count("/")
            for pattern in patterns:
                if "/" in pattern:
                    if fnmatch(rel, pattern):
                        found[group].add(rel)
                elif depth <= 1 and fnmatch(name, pattern):
                    found[group].add(rel)
    for rel in rel_strings:
        if rel.endswith("pyproject.toml") or rel.endswith("setup.cfg") or rel.endswith("package.json"):
            try:
                text = (repo / rel).read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for marker, group in PYPROJECT_SECTIONS.items():
                if marker in text:
                    found[group].add(f"{rel} ({marker.strip('[')})")
            if "[tool:pytest]" in text:
                found["Test configuration"].add(f"{rel} (tool:pytest)")
            if rel.endswith("package.json"):
                for key in ("jest", "vitest", "mocha", "playwright", "cypress", "eslint", "c8", "nyc", "coverageThreshold"):
                    if f'"{key}' in text:
                        found["Test configuration" if key not in {"eslint"} else "Static analysis"].add(f"{rel} ({key})")
    return {k: sorted(v) for k, v in found.items()}


def run_git(repo: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=60, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def git_signals(repo: Path, since: str) -> dict | None:
    if run_git(repo, ["rev-parse", "--is-inside-work-tree"]) is None:
        return None
    log = run_git(repo, ["log", f"--since={since}", "--no-merges", "--name-only", "--format=%x00%H%x01%s"])
    if log is None:
        return None
    churn: Counter[str] = Counter()
    fix_files: Counter[str] = Counter()
    commits = fix_commits = fix_with_tests = 0
    fix_re = re.compile(FIX_GREP, re.IGNORECASE)
    for block in log.split("\x00"):
        if not block.strip():
            continue
        header, _, body = block.partition("\n")
        _, _, subject = header.partition("\x01")
        changed = [line.strip() for line in body.splitlines() if line.strip()]
        commits += 1
        churn.update(changed)
        if fix_re.search(subject):
            fix_commits += 1
            fix_files.update(f for f in changed if not is_test_file(Path(f)))
            if any(is_test_file(Path(f)) for f in changed):
                fix_with_tests += 1
    existing = lambda c: [(f, n) for f, n in c.most_common(50) if (repo / f).exists()][:15]
    head = (run_git(repo, ["rev-parse", "--short", "HEAD"]) or "").strip()
    return {
        "since": since,
        "head": head,
        "commits": commits,
        "fix_commits": fix_commits,
        "fix_commits_that_changed_tests": fix_with_tests,
        "churn_hotspots": existing(churn),
        "fix_hotspots": existing(fix_files),
    }


def collect(repo: Path, since: str, max_files: int) -> dict:
    files = list(walk(repo, max_files))
    langs: Counter[str] = Counter()
    per_dir: dict[str, Counter] = defaultdict(Counter)
    source_sizes = []
    no_assert: list[str] = []
    skipped: Counter[str] = Counter()
    skip_res = [re.compile(p) for p in SKIP_PATTERNS]

    for rel in files:
        lang = LANGUAGES.get(rel.suffix.lower())
        if not lang:
            continue
        top = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        test = is_test_file(rel)
        langs[lang] += 1
        per_dir[top]["test" if test else "source"] += 1
        full = repo / rel
        if test:
            try:
                text = full.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            hits = sum(len(r.findall(text)) for r in skip_res)
            if hits:
                skipped[str(rel)] = hits
            if rel.suffix == ".py":
                no_assert.extend(f"{rel}::{name}" for name in python_tests_without_assert(full))
            elif rel.suffix in {".js", ".ts", ".jsx", ".tsx", ".mjs"} and js_tests_without_assert(text):
                no_assert.append(f"{rel} (no expect/assert in file)")
        else:
            source_sizes.append((str(rel), count_lines(full)))

    source_total = sum(c["source"] for c in per_dir.values())
    test_total = sum(c["test"] for c in per_dir.values())
    source_sizes.sort(key=lambda x: x[1], reverse=True)
    return {
        "repo": str(repo),
        "files_scanned": len(files),
        "truncated": len(files) >= max_files,
        "languages": langs.most_common(),
        "source_files": source_total,
        "test_files": test_total,
        "per_top_level_dir": {d: dict(c) for d, c in sorted(per_dir.items())},
        "configs": find_configs(repo, files),
        "tests_without_visible_assertion": no_assert[:50],
        "tests_without_visible_assertion_count": len(no_assert),
        "skipped_test_markers": skipped.most_common(20),
        "largest_source_files": source_sizes[:10],
        "git": git_signals(repo, since),
    }


def to_markdown(s: dict) -> str:
    out = [f"# Repo signals: {s['repo']}", ""]
    out.append(f"Files scanned: {s['files_scanned']}{' (truncated)' if s['truncated'] else ''}")
    out.append("Languages: " + (", ".join(f"{l} ({n})" for l, n in s["languages"]) or "none detected"))
    ratio = f"{s['test_files'] / s['source_files']:.2f}" if s["source_files"] else "n/a"
    out.append(f"Source files: {s['source_files']}, test files: {s['test_files']}, test/source ratio: {ratio}")
    out += ["", "## Files per top-level directory", "", "| Directory | Source | Test |", "|---|---|---|"]
    for d, c in s["per_top_level_dir"].items():
        out.append(f"| {d} | {c.get('source', 0)} | {c.get('test', 0)} |")
    out += ["", "## Configuration found", ""]
    for group in CONFIG_GROUPS:
        items = s["configs"].get(group, [])
        out.append(f"- **{group}:** " + (", ".join(items) if items else "none found"))
    out += ["", f"## Tests with no visible assertion ({s['tests_without_visible_assertion_count']})", ""]
    out += [f"- {t}" for t in s["tests_without_visible_assertion"]] or ["- none found"]
    out += ["", "## Skip / xfail / disabled markers", ""]
    out += [f"- {f}: {n}" for f, n in s["skipped_test_markers"]] or ["- none found"]
    out += ["", "## Largest source files (non-blank lines)", ""]
    out += [f"- {f}: {n}" for f, n in s["largest_source_files"]] or ["- none"]
    g = s["git"]
    out += ["", "## Git history", ""]
    if not g:
        out.append("- No git history available. Defect clustering cannot be measured from history.")
    else:
        out.append(f"- HEAD: {g['head']}, commits since {g['since']}: {g['commits']}")
        out.append(
            f"- Commits whose subject looks like a fix: {g['fix_commits']}, "
            f"of which changed a test file: {g['fix_commits_that_changed_tests']}"
        )
        out += ["", "Change hotspots (commits touching the file):", ""]
        out += [f"- {f}: {n}" for f, n in g["churn_hotspots"]] or ["- none"]
        out += ["", "Fix hotspots (fix commits touching the source file):", ""]
        out += [f"- {f}: {n}" for f, n in g["fix_hotspots"]] or ["- none"]
    out += ["", "These are leads for the audit. Check each one before you report it as a finding."]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("--since", default="12 months ago")
    parser.add_argument("--max-files", type=int, default=50000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir():
        print(f"Not a directory: {repo}", file=sys.stderr)
        return 2
    signals = collect(repo, args.since, args.max_files)
    print(json.dumps(signals, indent=2) if args.json else to_markdown(signals))
    return 0


if __name__ == "__main__":
    sys.exit(main())
