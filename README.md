# claude-marketplace

A marketplace of Claude Code plugins. No guarantee they work or are safe to use — try at your own risk.

## Install

```
/plugin marketplace add theopnv/plugins-from-theopnv
/plugin install fortytwo@plugins-from-theopnv
/plugin install testing-fundamentals@plugins-from-theopnv
```

## Plugins

### fortytwo

Skills for running a project-based, piscine-style learning workflow — the format used by these famous french programming schools.

- **create-pool** — builds a self-paced learning roadmap (a "piscine") for any topic: daily objectives, difficulty ramped from the operator's actual level, self-checks, and weekly exams, all generated from material the operator supplies.
- **create-project** — writes a fully-specified project brief for a pool checkpoint or standalone assignment: exact input/output, forbidden tools and approaches, worked examples, and a self-check.
- **moulinette** — grades a submission against its brief: runs/opens/recomputes the work, scores it 0–20 with an evidence-backed breakdown, and reports where points were lost — without handing over the fix.

The three hand off to each other (roadmap → brief → grade) but each also works standalone.

### testing-fundamentals

Gives Claude the knowledge of a Foundation Level software tester, based on the ISTQB® Certified Tester Foundation Level (CTFL) v4.0 syllabus.

- **test-auditor**: works in four modes.
  - **Audit**: examines a repo, runs its tests and coverage, analyses product risk, and writes `docs/test-audit-YYYY-MM-DD.md`. Findings are ordered by risk, each with evidence and a syllabus section reference.
  - **Test design**: derives test cases for a function or user story with equivalence partitioning, boundary value analysis, decision tables, state transitions, and ATDD, with coverage figures.
  - **Change review**: reviews a diff or PR with impact analysis, confirmation testing, and regression testing.
  - **Test management artifacts**: test plans, risk registers, estimates, test reports, and defect reports.

It reads code and runs tools, but it does not change source code, tests, or configuration. It uses only the concepts of the CTFL v4.0 syllabus.

ISTQB® is a registered trademark of the International Software Testing Qualifications Board. This plugin is not affiliated with or endorsed by ISTQB®. Its content is an original summary based on the Certified Tester Foundation Level Syllabus v4.0 (© ISTQB®, 2023). Get the syllabus at [istqb.org](https://www.istqb.org).
