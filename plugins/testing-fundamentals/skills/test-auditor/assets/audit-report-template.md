# Test audit: <project name>

<!-- Target: 1,500 to 2,500 words. Tables, one row per item, each fact once. Remove this comment. -->

<YYYY-MM-DD> · <commit or version> · Scope: <what was audited, what was not> · Method: independent audit that applies the ISTQB® CTFL v4.0 syllabus. Static review plus test execution and coverage measurement. No source code, test, or configuration was changed.

## 1. Summary

<3 to 5 sentences: the overall picture, the level of confidence that the current tests give, and the main reason.>

**Strengths to keep:** <one line, with evidence>

## 2. Context and assumptions (§1.4.2)

- **Context:** <domain and criticality, users, team and who tests, SDLC, tools, regulation: one line each, only what changes the risk>
- **Assumptions:** <what I assumed where I could not check or ask. The reader can correct these.>

## 3. Measurements

| Measure | Value | How |
|---|---|---|
| Test cases (passed / failed / skipped), run time | | <command> |
| Statement / branch coverage | | <tool> |
| Coverage of the high-risk modules | <module: stmt / branch, ...> | |
| Tests with no assertion | | |
| Static analysis | <findings, or "none configured"> | |
| Test levels and quadrants (§2.2.1, §5.1.7) | <one line: what exists, what is missing> | |

## 4. Product risk register (§5.2)

| ID | Product risk | Quality characteristic | L | I | Level | Evidence |
|---|---|---|---|---|---|---|

<Project risks for the testing, if any: one line each.>

## 5. Findings

<!-- Highest risk first. Process findings (CI, reviews, traceability, CM, defect management) go here too, in risk order. -->

| ID | Finding | Status | Evidence | CTFL concept (§) | Risk | Action and owner |
|---|---|---|---|---|---|---|
| F1 | | confirmed / hypothesis | <file:line, input → expected vs actual> | | | |

## 6. Test design for the top risks (§4)

<!-- Full tables for the 1 or 2 highest risks only. For other risks: technique, number of missing coverage items, one example. -->

### <risk ID>: <test object>

<Test basis, defects in the test basis (with a question each), technique, coverage of existing tests per technique: 2 to 4 lines.>

| ID | Traces to (risk, rule, or criterion) | Technique and coverage item | Input / sequence | Expected result (test basis) | Actual (if probed) | Priority |
|---|---|---|---|---|---|---|

## 7. Action plan

| # | Action | Reduces risk | Owner | Estimate (optional, a / m / b → E ± SD) |
|---|---|---|---|---|

**Proposed exit criteria (§5.1.3):** <criteria the team can check, ideally in CI, each linked to a risk>

## 8. Limits

Testing shows the presence of defects, not their absence (§1.3). This audit did not: <list>.

## Appendix: key commands

```
<only the commands that produced the evidence above, with a one-line result>
```

---
<sub>Based on the ISTQB® Certified Tester Foundation Level Syllabus v4.0. Not affiliated with or endorsed by ISTQB®.</sub>
