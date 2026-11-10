# Change review

How to review a diff, a branch, or a pull request from a testing point of view. This is static testing of the change (§3) followed by focused dynamic testing where you can run it. The output is a review in the chat.

## Step 1. Get the change and its intent

- Get the diff: `git diff <base>...<head>`, `gh pr diff <number>`, or a patch file from the user. Get the description, the linked issue, and the commit messages.
- Classify the change with the maintenance triggers (§2.3): modification (enhancement, correction, hot fix), upgrade or migration of the environment (dependencies, runtime, platform, data conversion), or retirement. A change can be several of these. Say which.
- Find the test basis for the intended behaviour: the issue, the story and its acceptance criteria, the specification, the README. If the intent is not written anywhere, say so: the reviewer cannot verify a change against nothing.

## Step 2. Impact analysis (§2.2.3)

Find what the change can affect beyond the lines that it touches:
- callers and users of each changed function, class, endpoint, configuration key, schema, or message (search the repo)
- shared data: database columns, files, caches, events that other components read
- interfaces with other systems (system integration level)
- the environment: build, dependencies, CI, deployment configuration
- changed constants, thresholds, defaults, and error handling, which often have effects far from the diff

Write the impact as a short list of areas, each with a risk level (§5.2). This list decides the scope of regression testing.

Also check whether the diff changes things that the description does not mention. An unannounced change in the same PR is a common source of regression, because nobody looks for its effects.

## Step 3. Confirmation testing (for a fix)

If the change fixes a defect:
- Is there a test that reproduces the original failure? It must fail before the fix and pass after it. If you can, check both: run it on the base and on the head (in a temporary copy, not in the user's working tree).
- Does the test use the exact conditions of the failure report?
- Does it cover the neighbourhood of the defect? A fix of a boundary needs BVA around that boundary (§4.2.2), not only the one value from the report. A fix of a rule needs the other columns of its decision table (§4.2.3). A fix of a transition needs the invalid transitions around it (§4.2.4).

## Step 4. Regression testing

- Do the existing tests cover the impacted areas from step 2? Name the tests, or say that there are none.
- Run the existing suite on the change if you can. Record the result.
- If you can, measure branch coverage of the changed lines: which new or changed branches does no test execute?
- List the regression test cases that are missing, highest risk first.

## Step 5. Test design for new or changed behaviour

Apply the techniques of `test-techniques.md` to the new or changed logic: EP and BVA for new inputs or thresholds, decision tables for new conditions, state transitions for new states or events, error guessing for the error handling. Compare with the tests in the diff. List the missing coverage items.

## Step 6. Static review of the change

Look for the defects that static testing finds well (§3.1.3): inconsistencies with the specification, duplicated or unreachable code, interface mismatches (parameters, types, order), deviations from the project's standards, and missing tests for an acceptance criterion. Look at the tests in the diff as work products too: do they assert the expected result from the test basis, or the current output?

## Step 7. Verdict

Choose one:
- **Ready**: the confirmation and regression risks are covered.
- **Ready with conditions**: list the tests or checks to add before or right after the merge, with their risk.
- **Not ready**: name the failure, the unacceptable risk, or the missing test basis.

The verdict is information for the person who decides. It is not a decision on their behalf.

## Output format

```markdown
## Test review: <PR title or change>

**Verdict:** Ready / Ready with conditions / Not ready. <one sentence why>

**Change type:** <maintenance trigger(s)>. **Test basis:** <issue, story, spec, or "none found">.

### What I ran
<commands and results: suite on base and head, coverage of changed lines, probes>

### Findings (highest risk first)
| ID | Finding | Evidence | CTFL concept (§) | Risk | Recommendation |

### Impact analysis
| Area affected | How | Existing tests | Risk level |

### Confirmation testing
<is there a test that reproduces the original failure; does it cover the neighbourhood>

### Missing test cases
| ID | Traces to (rule, issue, or criterion) | Technique and coverage item | Input / sequence | Expected result (from the test basis) | Priority |

### What works well
<strengths of the change, with evidence>

### Not checked
<limits>
```

Keep it short for a small change. A one-line fix with a correct confirmation test and no impact can have a three-line review.
