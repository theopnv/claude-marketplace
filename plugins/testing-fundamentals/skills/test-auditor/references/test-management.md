# Managing the test activities (syllabus chapter 5)

How to plan, estimate, prioritize, analyse risk, monitor, report, and manage defects. Templates for the deliverables are in `assets/`.

## Contents

1. Test plan (§5.1.1)
2. Release and iteration planning (§5.1.2)
3. Entry and exit criteria (§5.1.3)
4. Estimation (§5.1.4)
5. Test case prioritization (§5.1.5)
6. Test pyramid (§5.1.6)
7. Testing quadrants (§5.1.7)
8. Risk management (§5.2)
9. Monitoring, control, completion, metrics, reports (§5.3)
10. Configuration management (§5.4)
11. Defect management and defect reports (§5.5)

---

## 1. Test plan (§5.1.1)

A test plan describes the objectives, resources, and processes of the testing. It documents how and when the test objectives will be reached, helps the team meet the agreed criteria, communicates with the team and stakeholders, and shows that the testing follows the test policy and strategy (or explains why not). Writing it makes the planner think about risks, schedule, people, tools, cost, and effort.

Typical contents:
- **Context**: scope, test objectives, constraints, test basis
- **Assumptions and constraints**
- **Stakeholders**: roles, responsibilities, relevance to testing, hiring and training needs
- **Communication**: forms, frequency, templates
- **Risk register**: product risks and project risks
- **Test approach**: test levels, test types, test techniques, deliverables, entry and exit criteria, independence of testing, metrics, test data requirements, test environment requirements, deviations from the test policy and strategy
- **Budget and schedule**

Use `assets/test-plan-template.md`. Make the plan as light as the context allows: one page for a small team with CI, more for regulated or contractual work.

## 2. Release and iteration planning (§5.1.2)

In iterative SDLCs:
- **Release planning** looks ahead to a release, defines the product backlog, and can split large stories. Testers help write testable stories and acceptance criteria, take part in product and project risk analysis, estimate test effort, define the test approach, and plan the testing for the release.
- **Iteration planning** looks at one iteration backlog. Testers take part in the detailed risk analysis of stories, check that stories are testable, split stories into tasks (especially test tasks), estimate the test tasks, and refine the functional and non-functional aspects of the test object.

## 3. Entry and exit criteria (§5.1.3)

**Entry criteria** are the preconditions to start an activity. Without them, the activity is harder, slower, more expensive, and riskier. Typical: resources available (people, tools, environments, test data, budget, time); testware available (test basis, testable requirements, stories, test cases); initial quality of the test object (for example, all smoke tests pass).

**Exit criteria** say what must be true to call an activity complete. Typical:
- measures of thoroughness: coverage reached, number of unresolved defects, defect density, number of failed test cases
- completion criteria: planned tests executed, static testing done, all defects found reported, all regression tests automated

Define them per test level. Running out of time or budget can also be a valid exit criterion if the stakeholders reviewed and accepted the risk to release without more testing.

In Agile teams, exit criteria are the **Definition of Done** and entry criteria for a story are the **Definition of Ready**.

*On a codebase:* CI checks that block a merge are executable exit criteria (tests pass, coverage threshold, static analysis clean). A PR template checklist is a Definition of Done. Recommend criteria that the team can check automatically where possible, and link each one to a risk.

## 4. Estimation (§5.1.4)

An estimate depends on assumptions and always has an error. Say the assumptions. Small tasks are easier to estimate, so split a large task into small tasks and estimate each one.

| Technique | Type | How |
|---|---|---|
| **Ratios** | Metrics-based | Use ratios from past projects of the same organization. Example: if development to test effort was 3:2 before and development is 600 person-days now, test effort is about 400 person-days. |
| **Extrapolation** | Metrics-based | Measure early in the current project, then extrapolate. Example: the next iteration's test effort is the mean of the last three iterations. Good for iterative SDLCs. |
| **Wideband Delphi** | Expert-based | Each expert estimates alone. If the results differ more than the agreed range, the experts discuss, then estimate again alone. Repeat until consensus. **Planning Poker** is a variant with numbered cards. |
| **Three-point estimation** | Expert-based | Get an optimistic (a), most likely (m), and pessimistic (b) estimate. E = (a + 4m + b) / 6. Standard deviation SD = (b − a) / 6. Give the result as E ± SD. |

Three-point worked example (ours): a = 4, m = 7, b = 16 person-days. E = (4 + 28 + 16) / 6 = 8. SD = (16 − 4) / 6 = 2. The estimate is 8 ± 2 person-days (6 to 10).

For an audit action plan, give a three-point estimate per action when the user wants effort figures. Show the a, m, b values and the calculation so that the team can challenge them. You are one estimator: say that a Wideband Delphi or Planning Poker session with the team will give a better estimate.

## 5. Test case prioritization (§5.1.5)

Order the test cases in the execution schedule with one of these strategies:
- **Risk-based**: the test cases for the highest risks run first (from the risk analysis, §5.2.3).
- **Coverage-based**: the test cases with the highest coverage run first. Variant **additional coverage**: first the test case with the highest coverage, then each time the one that adds the most new coverage.
- **Requirements-based**: the test cases for the requirements that the stakeholders rank highest run first.

Dependencies override the order: if a high-priority test case needs a low-priority one, the low-priority one runs first. The availability of resources (tools, environments, people in a time window) also affects the order.

*On a codebase:* in CI, run the fast high-risk tests first so that a failure stops the pipeline early. In an action plan, the first tests to write cover the highest risks.

## 6. Test pyramid (§5.1.6)

The test pyramid shows that tests have different granularity. The bottom layer has many small, isolated, fast tests that each check a small piece of functionality. The top layer has few complex end-to-end tests that are slower and check large pieces of functionality. Higher layers have less isolation, coarser granularity, and longer execution time. The layers can have different names and numbers, for example unit / service / UI, or unit / integration / end-to-end.

*On a codebase:* count the tests per layer and measure their run time. Report the shape. An inverted pyramid (many slow end-to-end tests, few component tests) gives slow feedback and fragile suites. A pyramid with no top (no end-to-end or system tests) leaves the integration of the full system untested. Recommend the shape that fits the risks, not a fixed ratio.

## 7. Testing quadrants (§5.1.7)

Brian Marick's model groups test levels, test types, activities, techniques, and work products, mainly for Agile development. Two axes: business facing or technology facing, and support the team (guide development) or critique the product (measure it against expectations).

| | Support the team | Critique the product |
|---|---|---|
| **Business facing** | **Q2**: functional tests, examples, user story tests, user experience prototypes, API testing, simulations. Check acceptance criteria. Manual or automated. | **Q3**: exploratory testing, usability testing, user acceptance testing. User-oriented, often manual. |
| **Technology facing** | **Q1**: component and component integration tests. Automated and in CI. | **Q4**: smoke tests and non-functional tests (except usability). Often automated. |

*On a codebase:* place each group of existing tests in a quadrant. An empty quadrant is a finding if the product risks need it. Example: a public API with no Q4 tests (performance efficiency, security) and no Q3 activity.

## 8. Risk management (§5.2)

**Risk** (§5.2.1): a possible event, hazard, threat, or situation with a bad effect if it occurs. Two attributes: **risk likelihood** (probability, more than 0 and less than 1) and **risk impact** (the harm). Together they give the **risk level**. A higher level needs treatment first.

Main activities: **risk analysis** = risk identification + risk assessment; **risk control** = risk mitigation + risk monitoring. A test approach that selects, prioritizes, and manages the test activities with risk analysis and risk control is **risk-based testing**.

**Project risks and product risks** (§5.2.2):
- **Project risks** concern the management and control of the project: organizational issues (late deliveries, wrong estimates, cost cuts), people issues (missing skills, conflicts, communication, too few staff), technical issues (scope creep, poor tool support), supplier issues (a third party does not deliver, a vendor goes bankrupt). They affect the schedule, budget, or scope.
- **Product risks** concern the quality characteristics of the product (ISO/IEC 25010): missing or wrong functionality, wrong calculations, runtime errors, poor architecture, inefficient algorithms, slow response time, poor user experience, security vulnerabilities. Consequences: user dissatisfaction, lost revenue, trust, or reputation, damage to third parties, high maintenance costs, helpdesk overload, criminal penalties, and in extreme cases physical damage, injury, or death.

**Product risk analysis** (§5.2.3) makes the team aware of product risk so that the test effort minimizes the residual risk. Start it early.
- **Identification**: make a full list. Techniques: brainstorming, workshops, interviews, cause-effect diagrams. On a codebase you can also use the code, its history, the issues, and the documentation.
- **Assessment**: categorize each risk, determine likelihood, impact, and level, prioritize, and propose how to handle it. Risks in the same category usually need similar mitigation. Quantitative approach: level = likelihood × impact. Qualitative approach: a risk matrix.

Risk matrix used by this skill (1 = low, 3 = high):

| Likelihood \ Impact | 1 | 2 | 3 |
|---|---|---|---|
| **3** | 3 medium | 6 high | 9 high |
| **2** | 2 low | 4 medium | 6 high |
| **1** | 1 low | 2 low | 3 medium |

The results of the analysis decide: the scope of testing; the test levels and test types; the techniques and the coverage to reach; the effort per task; the order of testing (to find critical defects early); and whether activities other than testing are needed to reduce the risk.

**Product risk control** (§5.2.4) = **mitigation** (do the actions that reduce the risk level) + **monitoring** (check that the actions work, improve the assessment, find new risks). Responses: mitigation by testing, acceptance, transfer, or a contingency plan. Ways to mitigate by testing:
- choose testers with the correct experience and skills for the risk type
- apply a suitable level of independence of testing
- do reviews and static analysis
- apply suitable test techniques and coverage levels
- apply the test types for the affected quality characteristics
- do dynamic testing, including regression testing

Use `assets/risk-register-template.md` for the register.

## 9. Monitoring, control, completion, metrics, reports (§5.3)

**Test monitoring** collects information about the testing to assess progress and to check the exit criteria (for example coverage of product risks, requirements, or acceptance criteria). **Test control** uses that information to give **control directives**, for example: reprioritize tests when a risk becomes an issue; check again whether an item meets entry or exit criteria after rework; adjust the schedule when the test environment is late; add resources. **Test completion** collects data at milestones (end of a test level, an iteration, a project, a release, a maintenance release) to keep the experience, the testware, and other useful information.

**Metrics** (§5.3.1):
- project progress: task completion, resource usage, test effort
- test progress: test case implementation progress, environment preparation progress, test cases run / not run, passed / failed, execution time
- product quality: availability, response time, mean time to failure
- defects: number and priorities of defects found and fixed, defect density, defect detection percentage
- risk: residual risk level
- coverage: requirements coverage, code coverage
- cost: cost of testing, organizational cost of quality

**Test progress report** (§5.3.2), regular (daily, weekly): test period; progress against the plan and notable deviations; impediments and workarounds; metrics; new and changed risks; testing planned for the next period.

**Test completion report**, at completion when ideally the exit criteria are met: test summary; evaluation of testing and product quality against the test plan (objectives, exit criteria); deviations from the plan (schedule, duration, effort); impediments and workarounds; metrics from the progress reports; unmitigated risks and unfixed defects; lessons learned.

Adapt to the audience: frequent and informal inside the team, a set template for a completed project. Use `assets/test-report-template.md`.

**Communicating status** (§5.3.3): verbal, dashboards (CI/CD dashboards, task boards, burn-down charts), email and chat, online documentation, formal test reports. Distributed teams need more formal communication. Tailor the content to each stakeholder.

## 10. Configuration management (§5.4)

Configuration management (CM) identifies, controls, and tracks work products as **configuration items**: test plans, strategies, conditions, cases, scripts, results, logs, reports. For a complex item such as a test environment, CM records its parts, their relationships, and their versions. An approved item becomes a **baseline** and changes only through formal change control. CM lets you go back to a previous baseline to reproduce earlier test results.

CM makes sure that all configuration items, including the test items, are uniquely identified, version controlled, tracked for changes, and related to each other (for traceability), and that the test documentation references them unambiguously. In DevOps pipelines, CM is usually automated.

*On a codebase:* evidence of good CM: tests in the same repository as the code, lock files for dependencies, pinned versions of tools and runtimes, test environments defined as code (containers, compose files), tagged releases, test results linked to a commit. Evidence of weak CM: dependencies without versions, test data that only exists on one machine, environment setup described only in prose, test results that nobody can reproduce.

## 11. Defect management and defect reports (§5.5)

A defect management process has at least a **workflow** from discovery to closure and **rules for classification**. Typical workflow: log the anomaly, analyse and classify it, decide the response (fix, or keep as is), close the report. A reported anomaly can turn out to be a real defect, a false positive, or a change request. Everybody involved follows the process. Handle defects from static testing (including static analysis) the same way.

Objectives of a defect report: give the people who resolve it enough information; give a way to track the quality of the work product; give ideas to improve the development and test process.

**Contents of a defect report from dynamic testing:**
1. Unique identifier
2. Title with a short summary of the anomaly
3. Date of observation, issuing organization, author and their role
4. Identification of the test object and the test environment (version, commit, configuration, runtime)
5. Context: test case run, test activity, SDLC phase, test technique, checklist, or test data used
6. Description of the failure so that someone can reproduce and resolve it: the steps, and relevant logs, database dumps, screenshots, or recordings
7. Expected results and actual results
8. **Severity**: the degree of impact on the stakeholders or the requirements
9. **Priority**: how urgently to fix it
10. Status: for example open, deferred, duplicate, waiting to be fixed, awaiting confirmation testing, re-opened, closed, rejected
11. References: test case, requirement, story, related defects

Tools can fill some fields automatically (identifier, date, author, initial status).

**How to write a good one:**
- Reproduce the failure yourself first, with the smallest set of steps and data that show it. Include the exact command or input and the actual output.
- The title says what fails and where, not a guess about the cause: "Password reset link still works after its first use", not "Reset bug".
- Expected result: quote the test basis (rule ID, story, acceptance criterion). If the test basis is silent, say so: this can be a change request or a defect in the test basis.
- Justify severity and priority separately. High severity with low priority is possible (a crash in a feature that nobody uses yet), and so is the reverse (a wrong logo on the home page).
- Write facts about the product. No blame, no adjectives about the author (§1.5.1).
- A hypothesis about the location of the defect is useful, but label it as a hypothesis. Finding and fixing the defect is debugging, not testing (§1.1.2).
- Say which confirmation test proves the fix and which regression tests protect the related behaviour.

Use `assets/defect-report-template.md`.
