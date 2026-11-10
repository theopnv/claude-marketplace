# <ID>: <title: what fails, and where. No guess about the cause.>

| Field | Value |
|---|---|
| Identifier | <ID, or "assigned by the tracker"> |
| Date observed | <YYYY-MM-DD> |
| Author and role | <name, role> |
| Test object | <component, module, version, commit> |
| Test environment | <OS, runtime and version, configuration, data set> |
| Context | <test case, test activity, SDLC phase, technique or test data used> |
| Severity | <Critical / High / Medium / Low>. <why: impact on stakeholders or requirements> |
| Priority | <Immediate / High / Medium / Low>. <why: urgency to fix> |
| Status | Open |
| References | <requirement, rule, story, acceptance criterion, test case, related defects> |

## Description

<What happens, in 2 to 4 sentences. Facts about the product only.>

## Steps to reproduce

1. <precondition>
2. <action with exact input>
3. <observe>

<exact command or script, and its output>

## Expected result

<from the test basis, with a quote or rule ID. If the test basis is silent, say so.>

## Actual result

<observed output, with numbers>

## Attachments

<logs, output, screenshots>

## Notes for the fix (hypothesis)

<optional: where the defect probably is. Label it as a hypothesis. Finding and fixing the defect is debugging (§1.1.2).>

## Confirmation and regression testing

- **Confirmation test:** <the test that must fail now and pass after the fix>
- **Regression tests:** <related behaviour to protect, with the technique>
