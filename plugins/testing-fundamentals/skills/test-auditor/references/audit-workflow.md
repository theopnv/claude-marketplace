# Audit workflow

How to audit a repository's tests and test process, and produce `docs/test-audit-YYYY-MM-DD.md` with `assets/audit-report-template.md`.

The audit is a test project of its own. You plan it, you analyse, you design, you execute, and you report (§1.4.1). The steps below follow that order. Adapt the depth to the size of the repo and to the time the user gives you. For a large repo, audit the high-risk areas in depth and the rest at the surface, and say so in the limits.

## Step 1. Reconnaissance

Run the signal script first. It is read-only and needs only Python 3:

```bash
python3 <skill-dir>/scripts/repo_signals.py <repo-path>
```

It reports the languages, source and test file counts per top-level directory, test configuration, CI, static analysis configuration, review templates, environment and dependency files, test files with no visible assertion, skipped tests, the largest source files, and, if the repo has git history, the change hotspots and the files most often touched by fix commits. Treat its output as leads to check, not as findings.

Then read:
- the README, the docs, any specification, ADRs, user stories or feature files, issue and PR templates (the test basis and the process)
- the test configuration and the CI workflow (what runs, when, and what blocks a merge)
- a sample of test files from each layer (what they really assert)
- the source of the modules that look risky (from the hotspots, the size, the domain)

## Step 2. Context and questions (§1.4.2)

Write down what you infer for each context factor: stakeholders, team, business domain and criticality, technical factors, constraints, SDLC, tools. Then ask the 2 to 4 questions that matter most (see SKILL.md, rule 3). If you cannot ask, write assumptions.

## Step 3. Product risk analysis (§5.2.3)

Identify product risks from:
- **The domain**: what can go wrong for users and for the business. Money, data, security, legal, safety.
- **The ISO/IEC 25010 characteristics** (§2.2.2): for each one, ask if the product has a risk. Functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability. Skip the ones that do not apply and say why in one line.
- **Defect clustering** (§1.3): files often touched by fix commits, high churn, large or complex modules.
- **The test basis**: ambiguous or contradictory rules make wrong implementations likely.
- **Weak tests**: areas with no tests, tests with no assertion, only happy paths.

Assess each risk: likelihood 1-3, impact 1-3, level = product (matrix in `test-management.md`). Keep the list to the risks that matter, usually 5 to 15. Note project risks for the testing too (no test environment, one person knows the tests, no time for testing), but keep them separate from product risks (§5.2.2).

## Step 4. Measure (dynamic testing)

1. Find how the project runs its tests (CI file, Makefile, package scripts, pyproject, README). Use that command.
2. Check that the run is safe (SKILL.md, rule 2). If the project needs packages that are not installed, use an environment outside the project (for example a temporary virtual environment) or ask the user. Record the exact commands.
3. Run the suite. Record: the number of tests, passed, failed, skipped, errors, the run time.
4. Measure statement and branch coverage with the project's coverage tool or the standard one for the stack (see `test-techniques.md`, section 7). Record the coverage per module, and the missed branches in the high-risk modules.
5. Run the static analysis tools that the project configures, if they are installed. Record the number and the kind of findings. If no tool is configured, that is a finding (§3.1, §2.1.5).
6. If something fails, report the failure with its evidence. Do not fix it.

If you cannot run the tests, say why, and continue with static analysis of the code and tests. Mark each coverage figure as an estimate.

## Step 5. Assess the test process

Use this checklist (checklist-based review, §4.4.3). For each item, answer with evidence: yes, partly, no, or not applicable. Report only the items that give a finding or a strength. Do not paste the full checklist into the report.

**Test basis and static testing (§3)**
- Does a written test basis exist for the important behaviour (spec, stories with acceptance criteria, API contract, documented rules)?
- Does the test basis contain ambiguities, contradictions, or omissions? (Review it. Each one is a finding with a quote.)
- Is static analysis configured, and does it run in CI? Are its findings treated, or ignored?
- Is there a review process for code (required approvals, CODEOWNERS, PR template with a testing section)? Which review type does it look like (§3.2.4)?

**Test levels and test types (§2.2)**
- Which test levels exist (component, component integration, system, system integration, acceptance)? Which are missing where the risks need them?
- Which test types exist (functional, non-functional, black-box, white-box)? Is there any non-functional testing where the product risks need it (performance efficiency, security, reliability)?
- Are the boundaries between levels clear, or do the same checks repeat at several levels with no other objective?

**Test design quality (§4)**
- Do the tests in the high-risk modules show systematic techniques (partitions, boundaries, combinations, invalid transitions)? Or only happy paths?
- Does each test have an expected result that can fail? Count tests with no assertion or with assertions that cannot fail.
- Are the expected results derived from the test basis, or copied from the current output of the code?
- Do negative tests exist (invalid input, rejected events, error handling)?

**Pyramid and quadrants (§5.1.6, §5.1.7)**
- What is the shape of the pyramid (count and run time per layer)?
- Which quadrants have tests? Is an empty quadrant a risk for this product?

**Automation, CI, DevOps (§2.1.4, §6.2)**
- Does CI run the tests on each change? Does a failure block the merge (an executable exit criterion)?
- How long does the suite take? Fast feedback is the main benefit of CI.
- Are there automation risks: tools that nobody maintains, a suite that nobody keeps green, many skipped tests, results that are not repeatable?

**Confirmation, regression, maintenance (§2.2.3, §2.3)**
- When a defect is fixed, does a test that reproduces it get added? (Look at fix commits: do they change test files?)
- Is the regression suite automated and run in CI?
- Are maintenance triggers tested: dependency or runtime upgrades, data migrations?

**Traceability (§1.4.4)**
- Can you link requirements, stories, or issues to tests? (IDs in names or docstrings, feature files, a matrix.)
- Can the team answer "which requirement has no test?" today?

**Configuration management (§5.4)**
- Are dependencies locked? Are tool and runtime versions pinned?
- Is the test environment defined as code? Is test data versioned or generated by the tests?

**Defect management (§5.5)**
- Is there an issue template for defects with the fields of §5.5 (steps, expected and actual, environment, severity, priority)?
- Do fix commits reference defect reports?

**Planning, criteria, reporting (§5.1, §5.3)**
- Are there entry and exit criteria, Definition of Ready, or Definition of Done, written or enforced by CI?
- Is anything reported about testing (CI dashboard, coverage report, release notes with known defects)?

**Roles and independence (§1.4.5, §1.5)**
- Who tests what? Does anyone other than the author test the high-risk areas?
- Do business representatives take part in acceptance testing?

## Step 6. Test design for the top risks

For the 2 or 3 highest product risks, apply the techniques of `test-techniques.md` (section 10, "Find the gaps"). Do the full analysis for each one, so that your probes find the failures. In the report, give full test case tables only for the 1 or 2 highest risks. For each risk:
- the test object and the test basis
- the techniques that fit, the coverage items, and the coverage of the existing tests per technique
- the missing test cases, as a table with expected results from the test basis
- the result of the probes that you ran for the most important missing test cases (failures that you reproduced are confirmed findings)

This section makes the audit concrete. Generic advice ("add more edge cases") is not enough. Name the cases.

## Step 7. Write the report

Use `assets/audit-report-template.md`, and stay inside 1,500 to 2,500 words (SKILL.md, rule 10). Rules:
- Put all findings in one table, in order of risk level: product failures and process gaps together. Each row has an ID (F1, F2, ...), the status (confirmed or hypothesis), the evidence in one line, the CTFL concept and §, the risk, and the action with its owner role.
- Confirmed means that you saw the failure or the evidence. Hypothesis means that you suspect it from reading.
- Give the strengths in one line in the summary, with evidence.
- Write the action plan in order of risk, with an owner and, if useful, a three-point estimate (§5.1.4). Do not repeat the evidence there.
- Propose exit criteria that the team can enforce, linked to the risks (§5.1.3).
- End with the limits of the audit (§1.3, principle 1): what you did not run, not read, or could not check.
- Keep your probe scripts and full outputs outside the repo. The report quotes only the lines that prove a finding.

Then reply in the chat in at most 150 words: the verdict, the top 3 risks, the first actions, and the path of the report.
