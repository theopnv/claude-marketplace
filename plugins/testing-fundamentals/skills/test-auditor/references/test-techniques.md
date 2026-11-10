# Test analysis and design (syllabus chapter 4)

How to derive test cases in a systematic way, how to measure coverage, and how to find the gaps in an existing test suite. All examples are ours.

## Contents

1. The chain from test basis to test case
2. Choose the techniques
3. Equivalence partitioning (§4.2.1)
4. Boundary value analysis (§4.2.2)
5. Decision table testing (§4.2.3)
6. State transition testing (§4.2.4)
7. Statement and branch testing (§4.3)
8. Experience-based techniques (§4.4)
9. Collaboration-based approaches: user stories, acceptance criteria, ATDD (§4.5)
10. Find the gaps in an existing test suite
11. Output format for test design mode

---

## 1. The chain from test basis to test case

1. **Test basis**: the source of truth for the expected behaviour. Examples: a specification, a user story and its acceptance criteria, an API contract, a README, docstrings, an issue. If there is no written basis, use the code and the user's answers, and say that the expected results are assumptions.
2. **Test conditions**: what to test. Test analysis answers this question (§1.4.1).
3. **Coverage items**: the things that a technique counts. For example partitions, boundary values, decision table columns, transitions, branches.
4. **Test cases**: preconditions, inputs, and expected results that exercise the coverage items. Test design answers "how to test" (§1.4.1).
5. **Coverage** = coverage items exercised ÷ coverage items identified × 100%.

Always give the expected result from the test basis, not from the current behaviour of the code. A test that copies the current output of the code confirms the defects in it.

The techniques find defects in the test basis too. When you cannot decide the expected result for a coverage item, you found an ambiguity or an omission in the specification. Report it as a defect in the test basis (§1.4.3, test analysis work products) and ask the user.

## 2. Choose the techniques

Use several techniques together. Each one finds different defects.

| The test object has... | Use | Why |
|---|---|---|
| Inputs or outputs with ranges or categories (amounts, ages, sizes, types, roles) | Equivalence partitioning | Each partition is processed the same way, so one value per partition is enough |
| Ordered partitions (numbers, dates, lengths, counts) | Boundary value analysis | Developers often put a boundary at the wrong place or forget it |
| Combinations of conditions that give different outcomes (business rules, eligibility, pricing) | Decision table testing | Shows every combination, including the ones that the specification forgot |
| A lifecycle, a workflow, a session, a mode, a protocol | State transition testing | Shows the valid and the invalid sequences of events |
| Code to measure, or a specification that is vague or old | Statement and branch testing | Objective structural coverage; finds code that no test executes |
| History of defects, risky areas, little time | Error guessing, fault attacks | Uses knowledge of how software usually fails |
| Few or poor specifications, need to learn fast | Exploratory testing with charters | Design, execution, and learning at the same time |
| Recurring quality concerns (security basics, usability, coding errors) | Checklist-based testing | Consistent coverage of known concerns |
| A user story before or during implementation | ATDD with acceptance criteria | Prevents defects through shared examples |

Black-box tests stay valid when the implementation changes and the behaviour does not (§4.1). White-box tests depend on the code, but they measure what the black-box tests really executed. Experience-based tests find defects that both of the others miss. Use all three kinds.

## 3. Equivalence partitioning (EP, §4.2.1)

**Idea.** Divide each data element into partitions. The test object must process all values in a partition in the same way. If one value of a partition finds a defect, the other values in that partition must find it too. So one test case per partition is enough.

**Where.** Any data element: inputs, outputs, configuration items, internal values, time values, interface parameters. Partitions can be continuous or discrete, ordered or unordered, finite or infinite. They must not overlap and must not be empty.

**Valid and invalid partitions.** A valid partition contains values that the test object must process (or that the specification defines). An invalid partition contains values that the test object must reject or ignore (or that the specification does not define). Teams define these words differently. Say which definition you use.

**Procedure.**
1. List the data elements of the test object.
2. For each element, find the partitions from the test basis. Look at each rule, each threshold, each category, each type.
3. Mark each partition as valid or invalid.
4. Write test cases that cover each partition at least once. Cover each invalid partition in a separate test case, so that one rejection does not hide another (the same idea as fault masking in §4.2.4).

**Coverage.** Coverage items are the partitions, invalid partitions included. Coverage = partitions exercised ÷ partitions identified.

**Several data elements.** The simplest criterion is **Each Choice coverage**: each partition of each element appears in at least one test case. It does not cover combinations. Use a decision table when combinations matter.

**Example.** A cinema ticket price depends on age (integer): 0 to 11 child, 12 to 64 adult, 65 to 120 senior. Values below 0, above 120, or not integers are rejected.
- Valid partitions: child [0..11], adult [12..64], senior [65..120].
- Invalid partitions: below 0, above 120, not an integer.
- 6 coverage items, so at least 6 test cases. Example values: 5, 30, 80, -3, 150, "ten".

**Typical gap in existing tests.** One test per "interesting" value, all in the same valid partition, and no invalid partition at all.

## 4. Boundary value analysis (BVA, §4.2.2)

**Idea.** Test at the edges of ordered partitions, because developers often place a boundary one step too high or too low, or forget it. BVA works only for ordered partitions: if two values are in a partition, every value between them is in it too. The minimum and the maximum of a partition are its **boundary values**.

**Step size.** Find the smallest increment of the data: 1 for integers, 0.01 for amounts in cents, one day for dates, one character for lengths. Neighbours are one step away.

**2-value BVA.** For each boundary value, there are two coverage items: the boundary value and its nearest neighbour in the next partition.

**3-value BVA.** For each boundary value, there are three coverage items: the boundary value and both of its neighbours. It is more rigorous. It finds defects that 2-value BVA misses: for example, if `if (n <= 5)` was written as `if (n == 5)`, the 2-value tests n = 5 and n = 6 pass, but n = 4 from 3-value BVA fails.

**Coverage.** Coverage = coverage items exercised ÷ coverage items identified. Say which version (2-value or 3-value) you used. Use 3-value BVA for the high-risk boundaries.

**Procedure.**
1. Start from the EP partitions that are ordered.
2. For each boundary between two partitions, list the boundary values on each side (2-value) or each boundary value with both neighbours (3-value).
3. Remove duplicates: one value can be a coverage item for two boundaries.
4. Write a test case for each remaining value, with the expected result from the test basis.

**Example (cinema, 2-value).** Boundaries: -1|0, 11|12, 64|65, 120|121. Coverage items: -1, 0, 11, 12, 64, 65, 120, 121 (8 values).

**Example (amount, 3-value).** "A loan application needs a monthly income of at least 1500.00." Partitions: [0.00 .. 1499.99] rejected and [1500.00 .. max] accepted. Boundary values 1499.99 and 1500.00. 3-value coverage items: 1499.98, 1499.99, 1500.00 for the boundary 1499.99, and 1499.99, 1500.00, 1500.01 for the boundary 1500.00. After duplicates: 1499.98, 1499.99, 1500.00, 1500.01.

**Signs of boundary defects when you read code:** `>` against `>=`, `<` against `<=`, off-by-one in loops and slices, a constant that differs from the specification, the same boundary written in two places with two different operators, wording such as "over", "from", "up to", "at least" in the specification. Two documents that say "over 18" and "18 or older" for the same rule are a frequent ambiguity in the test basis.

## 5. Decision table testing (§4.2.3)

**Idea.** Business rules often say that combinations of conditions give different actions. A decision table lists them all, so no combination is forgotten.

**Structure.** The rows are the conditions and the actions. Each column is a **decision rule**: one unique combination of conditions with its actions.
- Conditions: `T` (true), `F` (false), `–` (the value has no effect on the outcome), `N/A` (the combination is not possible).
- Actions: `X` (the action occurs), blank (it does not occur).
- **Limited-entry** table: only Boolean values. **Extended-entry** table: conditions or actions can have several values (ranges, partitions, discrete values).

**Procedure.**
1. List the conditions (from the test basis) and the actions or outcomes.
2. Make the full table: 2^n columns for n Boolean conditions.
3. Remove the infeasible columns. You can merge columns where a condition has no effect (use `–`).
4. For each column, write the expected actions from the test basis. If the test basis gives no answer or two different answers for a column, you found a gap or a contradiction. Report it.
5. Write one test case per feasible column.

**Coverage.** Coverage items are the columns with feasible combinations. Coverage = columns exercised ÷ feasible columns.

**Size.** The number of columns grows exponentially. With many conditions, use a minimized table or choose the columns by risk.

**Example.** Account deletion: an administrator can delete any account. A user can delete their own account only when they have no open subscription and they confirmed their identity. With open subscriptions, the request is refused. Without identity confirmation, the system asks for it.

The full table has 2³ = 8 columns. When the requester is an administrator, the two other conditions have no effect, so 4 columns merge into R1. When a user has an open subscription, identity has no effect, so 2 columns merge into R2. The minimized table:

| Conditions | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Requester is administrator | T | F | F | F |
| Open subscription | – | T | F | F |
| Identity confirmed | – | – | T | F |
| **Actions** | | | | |
| Delete the account | X | | X | |
| Refuse: open subscription | | X | | |
| Ask for identity confirmation | | | | X |

Four test cases. While you build the table, ask the questions that the rule does not answer: can an administrator delete an account with an open subscription? Is the subscription cancelled or refunded first? Each unanswered column is a defect in the test basis.

## 6. State transition testing (§4.2.4)

**Model.** A **state transition diagram** shows the states and the valid transitions. An **event** starts a transition. A **guard condition** can restrict it. The transition can cause an **action**. Label syntax: `event [guard] / action`.

A **state table** shows the same model as a grid: rows are states, columns are events (with guards), cells give the target state and the action. Empty cells are **invalid transitions**. The table shows the invalid transitions explicitly, so it is the better tool for finding missing negative tests.

**Test cases** are sequences of events that cause sequences of state changes. One test case usually covers several transitions.

**Coverage criteria** (from weakest to strongest):
- **All states coverage**: each state is visited. Coverage = states visited ÷ states.
- **Valid transitions coverage** (0-switch coverage): each valid transition is exercised. Coverage = valid transitions exercised ÷ valid transitions. This is the most common criterion. 100% of it gives 100% all states coverage.
- **All transitions coverage**: each valid transition is exercised, and each invalid transition is attempted. Coverage = (valid exercised + invalid attempted) ÷ (all valid + all invalid). 100% of it gives 100% of the two others. Use it as the minimum for mission-critical and safety-critical software.

Attempt only one invalid transition per test case. If one test case attempts several, the first rejection can hide the next defect (**fault masking**).

**Procedure.**
1. From the test basis, list the states, the events, the guards, and the actions.
2. Draw the state table. Each cell that the test basis does not define is either an invalid transition or a gap in the specification. Ask if you cannot tell.
3. Choose the coverage criterion by risk.
4. Write event sequences that reach the criterion. Then add one test case per invalid transition (for all transitions coverage).
5. For each test case, give the expected state after each event, the expected actions, and, for invalid events, the expected rejection and the unchanged state.

**Example.** A document workflow with the states DRAFT, IN_REVIEW, APPROVED, PUBLISHED, ARCHIVED and the events submit, approve, reject, publish, archive. Valid: DRAFT-submit→IN_REVIEW, IN_REVIEW-approve→APPROVED, IN_REVIEW-reject→DRAFT / notify author, APPROVED-publish→PUBLISHED, PUBLISHED-archive→ARCHIVED. With 5 states and 5 events, the state table has 25 cells: 5 valid transitions and 20 invalid ones (including all events in the final state ARCHIVED).
- All states: submit, approve, publish, archive (1 test case visits all 5 states, but misses the reject transition).
- Valid transitions: submit, reject, submit, approve, publish, archive (1 test case covers all 5 valid transitions).
- All transitions: add 20 test cases, one invalid event each, for example "publish in IN_REVIEW is rejected and the state stays IN_REVIEW".

**Typical gap in existing tests.** Only the happy path; no test for invalid events; no test for the final states.

## 7. Statement and branch testing (§4.3)

**Statement testing.** Coverage items are the executable statements. Coverage = statements executed ÷ executable statements. 100% means each statement ran at least once, so a statement with a defect ran at least once. It can still miss defects that depend on data (a division that fails only when the divisor is zero), and it does not guarantee that each decision took both outcomes.

**Branch testing.** A **branch** is a transfer of control between two nodes of the control flow graph. It is unconditional (straight-line code) or conditional (an outcome of an `if`, of a `switch`/`case`, or of a loop: continue or exit). Coverage items are the branches. Coverage = branches exercised ÷ branches. 100% branch coverage gives 100% statement coverage, but the reverse is not true. Branch coverage can still miss defects that need a specific path through the code.

**Value of white-box testing** (§4.3.3). It considers the full implementation, so it finds defects even when the specification is vague, old, or incomplete. Its weakness: it cannot find a requirement that nobody implemented (defects of omission). It also works statically: you can walk through code, pseudocode, or a control flow graph without running it. Only white-box measures give an objective view of code coverage. Black-box testing alone cannot tell what code ran.

**On a codebase.**
- Measure, do not guess. For Python: `coverage run --branch -m pytest` then `coverage report -m` (or `pytest --cov --cov-branch` with pytest-cov). For JavaScript or TypeScript: the coverage option of the test runner (Jest, Vitest, c8). For Go: `go test -cover` gives statement coverage only, so say so. For Java: JaCoCo gives branch coverage.
- Report statement and branch coverage per module, and list the missed branches in the high-risk modules. A missed branch in a pricing rule matters more than 20 missed lines in a logging helper.
- High coverage with weak assertions is a false comfort: the code ran, but nothing compared actual and expected results. Look at the assertions, not only the percentage.
- A coverage target has value only if it is linked to risk. Do not recommend "80% everywhere". Recommend branch coverage targets for the high-risk modules.

## 8. Experience-based techniques (§4.4)

**Error guessing** (§4.4.1). Anticipate errors, defects, and failures from knowledge of how this application failed before, which errors developers usually make, and which failures occurred in similar applications. Categories to scan:
- input: correct input rejected, parameters wrong or missing
- output: wrong format, wrong result
- logic: missing cases, wrong operator
- computation: wrong operand, wrong formula, rounding
- interfaces: parameter mismatch, incompatible types
- data: wrong initialization, wrong type

A **fault attack** is the methodical form: make or get a list of possible errors, defects, and failures, then design tests that expose each one. Build the list from experience, defect data (fix commits, issue tracker), and common knowledge about why software fails.

**Exploratory testing** (§4.4.2). Design, execute, and evaluate tests at the same time while you learn about the test object. Useful when the specifications are few or poor, when time is short, and to complement formal techniques. **Session-based testing** gives it structure: a time-box, a **test charter** with the test objectives, notes on a test session sheet, and a debriefing with the stakeholders. The charter's objectives act as high-level test conditions. Exploratory testing can use the other techniques inside the session.

Charter template:
```
Charter: Explore <target area> with <resources, data, tools> to discover <information: risks, failures, questions>.
Time-box: 60 min. Tester: <name>. Debrief with: <stakeholder>.
```

**Checklist-based testing** (§4.4.3). Design and run tests to cover the test conditions of a checklist. Build the checklist from experience, from what matters to users, or from knowledge of why software fails. Write each item as a question that a person can check directly and separately. Do not put in a checklist items that a tool can check, items that are really entry or exit criteria, or items that are too general. Update the checklist from defect analysis and keep it short. High-level checklists give more variation (more coverage, less repeatability).

## 9. Collaboration-based approaches (§4.5)

These approaches focus on **defect avoidance** through collaboration, in addition to defect detection.

**User stories** (§4.5.1). The "3 C's": **Card** (the medium), **Conversation** (how the software will be used), **Confirmation** (the acceptance criteria). Usual format: "As a [role], I want [goal], so that [business value]", followed by the acceptance criteria. Write them together, from the business, development, and testing points of view. A good story is **INVEST**: Independent, Negotiable, Valuable, Estimable, Small, Testable. If a stakeholder does not know how to test a story, the story is probably unclear or without value to them.

**Acceptance criteria** (§4.5.2) are the conditions that the implementation must meet for the stakeholders to accept it. They are the test conditions of the story. They define its scope, give consensus, describe positive and negative scenarios, are the basis of acceptance testing, and allow planning and estimation. Two common formats:
- **Scenario-oriented**: Given/When/Then (as in BDD).
- **Rule-oriented**: a verification list of bullet points, or a table of inputs and outputs.
Any other format is acceptable if it is clear and has no ambiguity.

**ATDD** (§4.5.3) is test-first:
1. **Specification workshop**: the team (business, developers, testers) analyses the story and writes or completes the acceptance criteria. Remove ambiguities, gaps, and defects now.
2. **Create the test cases** from the acceptance criteria, as a team or by the tester. The test cases are examples of how the software must work.
3. Order: positive test cases first (the normal flow, no errors), then **negative** test cases, then **non-functional** characteristics (for example performance efficiency, usability).
4. Write them in language that the stakeholders understand: preconditions, inputs, postconditions.
5. Cover all the characteristics of the story, and no more. No two test cases cover the same characteristic. Use EP, BVA, decision tables, state transitions, and experience-based techniques to choose the examples.
6. If they are in a format that a test automation framework supports, developers can automate them while they implement the story. They become **executable requirements**.

## 10. Find the gaps in an existing test suite

This is the main use of the techniques in an audit and a change review.

1. Choose the test objects by risk (the high-risk modules, the changed code).
2. Find the test basis for each one (spec, README, story, docstrings, issue). Note ambiguities, contradictions, and omissions as defects in the test basis.
3. Apply the techniques that fit (section 2) and list the coverage items.
4. Map each existing test case to the coverage items that it exercises. Read the assertions: a test with no assertion, or an assertion on the wrong thing, exercises nothing that it can detect.
5. Calculate the coverage per technique, for example "EP 3/6 partitions (50%), 2-value BVA 1/8 boundary values (12.5%), valid transitions 3/5 (60%), all transitions 3/20 (15%)".
6. List the missing coverage items as recommended test cases, highest risk first.
7. Where possible, run a probe for the missing coverage items with the highest risk. A failure that you reproduce becomes a confirmed finding with evidence.
8. Add white-box data: missed branches in the same modules, from a coverage run.

## 11. Output format for test design mode

```markdown
## Test design: <test object>

**Test basis:** <documents used>. **Assumptions:** <where the basis is silent>.
**Defects in the test basis:** <ambiguities, gaps, contradictions, with a question for each>

### Test conditions
| ID | Test condition | Source | Risk level |

### Techniques and coverage items
For each technique: why you chose it, the model (partitions, boundaries, decision table, state table), the coverage items, the coverage criterion.

### Test cases
| ID | Traces to (test condition, and requirement or acceptance criterion) | Technique and coverage items | Preconditions | Inputs / event sequence | Expected result | Priority |

### Coverage
| Technique | Criterion | Items covered / identified | % |
| Existing tests (if any) | ... | ... | ... |

### Not covered, and why
<what these techniques cannot find, what you left out because of risk, what needs other test levels or test types>
```

Fill "Traces to" in every row, with the test condition ID and the requirement or acceptance criterion ID of the test basis (for example "C4, AC1"). Test cases from error guessing that no requirement covers trace to their test condition and say "no requirement" (§1.4.4: traceability shows which requirement has tests and which test has no requirement). Priority follows the risk level of the test condition (§5.1.5). If the user asks for code, add test code that implements the table, with one test function per test case or a parametrized test whose IDs match the table, so that the traceability stays visible.
