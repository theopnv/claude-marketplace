# CTFL v4.0 concepts map

A summary of chapters 1, 2, 3, and 6 of the syllabus, in our own words, with notes on how to use each concept on a codebase. Chapter 4 (techniques) is in `test-techniques.md`. Chapter 5 (test management) is in `test-management.md`.

## Contents

1. Testing basics (§1.1, §1.2)
2. The seven principles (§1.3)
3. Test process, testware, traceability (§1.4)
4. Roles, skills, whole team, independence (§1.4.5, §1.5)
5. Testing in the SDLC (§2.1)
6. Test levels and test types (§2.2)
7. Confirmation, regression, maintenance testing (§2.2.3, §2.3)
8. Static testing and reviews (§3)
9. Tools and automation (§6)

---

## 1. Testing basics

**Testing** (§1.1) is a set of activities that finds defects and evaluates the quality of work products. It is more than running tests: planning, analysis, design, reviews, and reporting are testing too. It includes **verification** (does it meet the specified requirements?) and **validation** (does it meet the needs of users and stakeholders in its real environment?). **Dynamic testing** executes the software. **Static testing** (reviews and static analysis) does not.

**Typical test objectives** (§1.1.1): evaluate work products (requirements, stories, designs, code); cause failures and find defects; reach the required coverage; reduce the risk of poor quality; verify the specified requirements; verify compliance with contracts, laws, and regulations; give stakeholders information for decisions; build confidence; validate that the test object is complete and works as the stakeholders expect. The objectives change with the context.

*On a codebase:* ask which objectives the current tests serve. A suite of unit tests on helpers builds some confidence but does not validate user needs and does not check compliance.

**Testing and debugging** (§1.1.2) are different activities. Testing causes failures (dynamic) or finds defects directly (static). Debugging reproduces the failure, finds the cause, and fixes it. After a fix, confirmation testing checks the fix, and regression testing checks that nothing else broke. As a tester, you report failures and evidence. You can give a hypothesis about the location of the defect, but the fix is a debugging task for the author.

**Testing and QA** (§1.2.2): testing is a form of **quality control** (product-oriented, corrective). **Quality assurance** is process-oriented and preventive: a good process gives a good product. Everybody on the project is responsible for QA. Test results feed both: QC uses them to fix defects, QA uses them to improve the process.

**Error, defect, failure, root cause** (§1.2.3): a person makes an **error** (time pressure, complexity, fatigue, lack of training). The error puts a **defect** into a work product: a requirement, code, a test script, a build file. A defect that executes can cause a **failure**. Some defects fail every time, some only under specific conditions, some never. Environmental conditions can also cause failures. **Root cause analysis** finds the basic reason. If you remove the root cause, similar defects become less frequent.

*On a codebase:* a defect in a requirement (an ambiguity in a README or a story) usually produces defects in the code and in the tests later. Look for them together.

## 2. The seven principles (§1.3)

| # | Principle | What it means for an audit |
|---|---|---|
| 1 | Testing shows the presence of defects, not their absence | Never say "fully tested" or "bug-free". Green tests reduce the probability of undetected defects. They do not prove correctness. |
| 2 | Exhaustive testing is impossible | Use test techniques, prioritization, and risk-based testing to focus the effort. A recommendation to "test all combinations" is almost always wrong. |
| 3 | Early testing saves time and money | Look for static testing (reviews, static analysis) and tests written with or before the code. A defect found in a story costs less than the same defect found in production. |
| 4 | Defects cluster together | A few components contain most defects. Use the git history (fix commits, churn) and complexity to find these clusters and to raise their likelihood in the risk analysis. |
| 5 | Tests wear out | Tests that repeat the same data find fewer new defects over time. Change test data and add new tests. Automated regression tests are the exception: there, repetition is the goal. |
| 6 | Testing is context dependent | A payment service and an internal script need different testing. Adapt the depth and formality to the context. |
| 7 | Absence-of-defects fallacy | Software can pass all its tests and still fail its users. Verification needs validation (acceptance tests, user feedback). |

## 3. Test process, testware, traceability

**Test activities** (§1.4.1). In practice they overlap and repeat:

| Activity | Question it answers | Main outputs (testware, §1.4.3) |
|---|---|---|
| Test planning | What are the objectives, and which approach reaches them within the constraints? | Test plan, schedule, risk register, entry and exit criteria |
| Test monitoring and control | Are we on plan? What must change? | Progress reports, control directives, risk information |
| Test analysis | What to test? | Prioritized test conditions (for example acceptance criteria), defect reports on the test basis |
| Test design | How to test? | Prioritized test cases, test charters, coverage items, test data and environment requirements |
| Test implementation | Is everything ready to run? | Test procedures, automated test scripts, test suites, test data, execution schedule, environment elements (stubs, drivers, simulators, service virtualization) |
| Test execution | What happened? | Test logs, defect reports |
| Test completion | What did we learn, and what do we keep? | Test completion report, improvement actions, lessons learned, change requests |

Test analysis also evaluates the test basis itself for defects and for **testability**.

**Context factors** (§1.4.2) that shape the test process: stakeholders, team members (skills, experience, availability), business domain (criticality, risks, regulation), technical factors (type of software, architecture, technology), project constraints (scope, time, budget), organization (structure, policies), SDLC (engineering practices), tools. These factors decide the test strategy, the techniques, the amount of automation, the coverage needed, the level of detail of the documentation, and the reporting.

**Traceability** (§1.4.4) links test basis elements to test conditions, risks, test cases, results, and defects. It lets you measure coverage (which requirement has tests?), estimate residual risk (which risk has passing tests?), analyse the impact of a change, and write reports that stakeholders understand.

*On a codebase:* look for links between requirements or stories and tests (issue IDs in test names or docstrings, BDD feature files, acceptance criteria in tests). If there are none, nobody can say which requirement has tests.

## 4. Roles, skills, whole team, independence

**Roles** (§1.4.5): the **test management role** is responsible for the test process, the team, and the test activities: mainly planning, monitoring and control, and completion. The **testing role** is responsible for the technical work: analysis, design, implementation, and execution. A team lead, a test manager, or a development manager can take the test management role. One person can hold both roles.

**Generic skills** (§1.5.1): testing knowledge; thoroughness, care, curiosity, attention to detail, method; communication, active listening, team play; analytical and critical thinking, creativity; technical knowledge; domain knowledge. Testers often bring bad news. Confirmation bias makes people reject information that disagrees with their beliefs. So communicate defects and failures in a constructive way.

**Whole team approach** (§1.5.2): any team member with the necessary skills can do any task, and everyone is responsible for quality. Testers work with business representatives on acceptance tests and with developers on the test strategy and automation. This approach is not always correct: safety-critical contexts can need high independence.

**Independence of testing** (§1.5.3): levels from none to very high are: the author tests; a peer in the same team tests; testers outside the team but in the organization test; testers from outside the organization test. Most projects should use several levels, for example developers at component and component integration level, a test team at system and system integration level, business representatives at acceptance level.
- Benefits: independent testers see other kinds of failures because they have other backgrounds and biases. They can challenge the assumptions of the authors.
- Drawbacks: isolation from the developers, poor communication, an adversarial relationship, developers who feel less responsible for quality, testers seen as a bottleneck.

*On a codebase:* if the same people write the code and all its tests, and nobody else reviews or tests, say so and recommend more independence for the high-risk areas only.

## 5. Testing in the SDLC

**Impact of the SDLC** (§2.1.1): the SDLC changes the scope and timing of test activities, the level of detail of documentation, the techniques, the amount of automation, and the role of the tester. Sequential models: testers review requirements and design tests early, but dynamic testing comes late. Iterative and incremental models: each iteration can use static and dynamic testing at all levels, so fast feedback and much regression testing are necessary. Agile: little documentation, much automation, and manual testing mostly with experience-based techniques.

**Good practices for any SDLC** (§2.1.2): each development activity has a matching test activity; each test level has its own objectives, so testing is complete without redundancy; test analysis and design for a level start during the matching development phase; testers review work products as soon as drafts exist.

**Test-first approaches** (§2.1.3):
- **TDD**: write a test, write the code that passes it, then refactor both.
- **ATDD**: derive tests from acceptance criteria during system design, before the code (details in `test-techniques.md`).
- **BDD**: describe the expected behaviour in simple natural language, usually Given/When/Then, then convert it to executable tests.
The tests stay as automated tests and protect later changes.

**DevOps** (§2.1.4) joins development, testing, and operations around common goals, with CI and CD. Benefits for testing: fast feedback, component tests and static analysis at each commit (shift-left), stable test environments from automated pipelines, more attention to non-functional characteristics, less repetitive manual testing, lower regression risk. Risks: someone must build and maintain the pipeline and the tools, and automation needs resources. Manual testing from the user's point of view is still necessary.

**Shift-left** (§2.1.5) means testing earlier, not testing less later. Practices: review specifications from a testing point of view; write test cases before code and run the code in a test harness; use CI/CD with automated component tests; run static analysis before dynamic testing or automatically; start non-functional testing at component level where possible. It costs more early and saves more later. Stakeholders must agree with it.

**Retrospectives** (§2.1.6): at the end of an iteration, release, or project, the team asks what worked, what did not, and how to keep the good and improve the rest. The results go into the test completion report, and someone must follow up the improvements. Benefits: more effective and efficient testing, better testware, team learning, a better test basis, better cooperation between development and testing.

*On a codebase:* CI config, branch protection, pre-commit hooks, and static analysis configuration are direct evidence of shift-left and DevOps practice. Their absence is a finding.

## 6. Test levels and test types

**Test levels** (§2.2.1) are instances of the test process at a given stage. Each has its own test object, objectives, test basis, typical defects and failures, approach, and responsibilities.

| Level | Focus | Typical owner | How to see it in a repo |
|---|---|---|---|
| Component (unit) testing | One component in isolation, with a harness or unit test framework | Developers | Fast tests of single functions or classes, stubs for dependencies |
| Component integration testing | Interfaces and interactions between components. Depends on the integration strategy (bottom-up, top-down, big-bang) | Developers | Tests that call several real modules together, a real database in a container |
| System testing | Behaviour and capabilities of the full system: end-to-end tasks and non-functional characteristics | Often an independent test team | Tests through the public interface (HTTP API, CLI, UI) of the deployed system |
| System integration testing | Interfaces with other systems and external services | Testers | Tests against real or virtualized external services in an environment close to production |
| Acceptance testing | Validation and readiness for deployment: does it meet the business needs? Forms: user acceptance, operational acceptance, contractual and regulatory acceptance, alpha, beta | Intended users, business representatives | Feature files, acceptance criteria checks, UAT records, operational checks (backup, restore, deployment) |

**Test types** (§2.2.2) can apply at every level:
- **Functional testing**: what the system does. Checks functional completeness, correctness, and appropriateness.
- **Non-functional testing**: how well it behaves. ISO/IEC 25010 characteristics: performance efficiency, compatibility, usability, reliability, security, maintainability, portability. Many non-functional tests reuse functional tests and add a constraint (for example a time limit). Non-functional defects found late are a serious threat to a project.
- **Black-box testing**: derived from specifications outside the test object. Checks behaviour against the specification.
- **White-box testing**: derived from the internal structure (code, architecture, workflows, data flows). Aims at structural coverage.

*On a codebase:* classify the existing tests by level and type. A common result: only component tests, only functional, nothing for security or performance even where the product risks need them.

## 7. Confirmation, regression, maintenance testing

**Confirmation testing** (§2.2.3) checks that the fix removed the original defect: run the tests that failed again, and add tests for the parts of the code that the fix changed. With little time, at least run again the steps that reproduced the failure.

**Regression testing** checks that a change (including a fix) did not have a bad effect in the same component, in other components, in connected systems, or in the environment. Do an **impact analysis** first to choose the scope. Regression suites run many times and grow, so they are strong candidates for automation, early, and in CI.

**Maintenance testing** (§2.3): maintenance can be corrective, adaptive (to a changed environment), or improve performance or maintainability. It includes planned releases and hot fixes. It tests the change and checks for regressions in the unchanged parts. Its scope depends on the risk of the change, the size of the system, and the size of the change. Triggers:
- **Modification**: planned enhancement, correction, hot fix.
- **Upgrade or migration** of the environment (new platform, new runtime, new dependency versions), including data conversion.
- **Retirement**: data archiving, and restore and retrieval procedures if the data must stay available.

*On a codebase:* dependency upgrades, runtime upgrades, and database migrations are maintenance triggers. Check that tests exist for them, not only for features.

## 8. Static testing and reviews

**Static testing** (§3.1) evaluates work products without executing them: manual reviews or tool-based static analysis. Almost any work product can be reviewed: requirements, stories, code, test plans, test cases, backlog items, charters, documentation, contracts, models. Static analysis needs a formal structure (code, models, formal text). Static analysis is often in CI and also evaluates maintainability and security.

**Value** (§3.1.2): finds defects in the earliest phases; finds defects that dynamic testing cannot find (unreachable code, design patterns not followed, defects in non-executable work products); builds a shared understanding among stakeholders. Reviews cost effort, but projects usually cost less overall with them.

**Static versus dynamic** (§3.1.3): static testing finds defects directly; dynamic testing causes failures, and analysis then finds the defects. Static testing reaches paths that are rarely executed and work products that cannot execute, and measures characteristics like maintainability. Dynamic testing measures characteristics that need execution, like performance efficiency. Defects that static testing finds more easily or cheaply:
- requirement defects: inconsistencies, ambiguities, contradictions, omissions, inaccuracies, duplications
- design defects: inefficient database structures, poor modularization
- some coding defects: undefined or undeclared variables, unreachable or duplicated code, too much complexity
- deviations from standards (naming conventions)
- incorrect interface specifications (number, type, or order of parameters)
- some security vulnerabilities (buffer overflows)
- gaps in test basis coverage (an acceptance criterion with no test)

**Early and frequent stakeholder feedback** (§3.2.1) prevents misunderstandings and lets the team focus on the most valuable features.

**Review process** (§3.2.2, based on ISO/IEC 20246): planning (scope, purpose, work product, quality characteristics, focus areas, exit criteria, effort, timeframe); review initiation (everyone has access and knows their role); individual review (each reviewer logs anomalies, recommendations, and questions, with techniques such as checklist-based or scenario-based reviewing); communication and analysis (decide status, owner, and action for each anomaly, and the quality level of the work product); fixing and reporting (a defect report for each defect, accept the work product when the exit criteria are met).

**Review roles** (§3.2.3): manager (decides what to review, gives resources); author (creates and fixes the work product); moderator or facilitator (runs the meetings, keeps time, keeps the environment safe); scribe or recorder (collects anomalies and decisions); reviewer (does the review: project member, subject matter expert, or other stakeholder); review leader (overall responsibility: who, when, where).

**Review types** (§3.2.4), from least to most formal:
- **Informal review**: no defined process, no formal output. Objective: find anomalies.
- **Walkthrough**: the author leads. Objectives: evaluate quality, build confidence, educate reviewers, get consensus, generate ideas, find anomalies.
- **Technical review**: technically qualified reviewers, a moderator leads. Objectives: consensus and decisions on a technical problem, plus finding anomalies and evaluating quality.
- **Inspection**: the full process, the most formal. Objective: find the maximum number of anomalies. Metrics are collected to improve the process. The author cannot be the review leader or the scribe.
Choose the type by objectives, SDLC, process maturity, criticality and complexity of the work product, regulation, need for an audit trail, and culture.

**Review success factors** (§3.2.5): clear objectives and measurable exit criteria (never evaluate the participants); the correct review type; small chunks; feedback to authors and stakeholders; enough preparation time; management support; reviews as part of the culture; training; facilitated meetings.

*On a codebase:* pull request reviews are usually informal reviews or technical reviews. Evidence: PR templates, CODEOWNERS, required approvals, review comments in the history. A PR template with a testing checklist is a cheap improvement. Also review the test basis (README, specs, stories) for ambiguities and contradictions: that is static testing, and it often explains code defects.

## 9. Tools and automation

**Tool categories** (§6.1): management tools (SDLC, requirements, tests, defects, configuration); static testing tools (reviews, static analysis); test design and implementation tools (generate test cases, data, procedures); test execution and coverage tools; non-functional testing tools; DevOps tools (pipeline, builds, CI/CD); collaboration tools; tools for scalability and standard deployment (virtual machines, containers); any other tool that helps (a spreadsheet can be a test tool).

**Benefits of test automation** (§6.2): less repetitive manual work (regression runs, data entry, result comparison, coding standard checks); consistency and repeatability; objective measures such as coverage; easier access to test information for management and reporting; shorter execution time, so earlier defect detection and faster feedback; more tester time for new and deeper tests.

**Risks of test automation** (§6.2): unrealistic expectations; low estimates of the cost to introduce the tool, maintain scripts, and change the process; automation where manual testing is more suitable; too much trust in the tool and no critical thinking; dependency on a vendor; open-source tools that nobody maintains any more or that need frequent updates; a tool that is not compatible with the platform; a tool that does not meet regulatory or safety requirements.

*On a codebase:* evaluate the automation that exists against these risks. A large end-to-end suite that nobody can keep green, or a test framework that is no longer maintained, are automation risks to report.
