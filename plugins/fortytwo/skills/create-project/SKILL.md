---
name: create-project
description: Writes a fully-specified piscine-style project brief — exact input, exact expected output, forbidden functions and approaches, worked examples, self-check, and a bonus section — for any topic, software or not. Use this whenever the operator wants a project brief, subject, spec, assignment, or capstone written up; asks to "turn this into a project", "write me a subject for X", "give me something to build with what I just learned"; hands over learning material and wants substantial practice work generated from it; or reaches a point in a learning pool where the integrative project that create-pool deliberately refuses to write is needed — even if they never say the word "brief".
---

# Create Project

A project brief — a *subject*, in piscine vocabulary — is the document a learner is handed on day one and argues with for the next two weeks. It works because it is closed: the input is pinned down, the output is pinned down, the shortcuts are named and banned, and every place the spec could be read two ways has been legislated in advance. A learner who finishes it knows they finished it. A grader who reads it knows what passing means. Nobody negotiates.

That closure is the whole product. A brief that says "build a tool that finds the largest square in a grid" is a prompt; a brief that says the first line holds the row count, `.` is empty and `o` is an obstacle, all rows are equal length, ties go to the topmost then leftmost square, and the only syscalls you may use are `open read write close malloc free exit stat` — that is a subject. Your job is to produce the second kind, for any topic: C, C++, accounting, GIMP, negotiation, epidemiology...

You author the *specification*. You do not author the solution, and you do not grade the result.

## Where this sits

- **`create-pool`** builds the roadmap and the daily exercises, and explicitly stops short of full projects — it hands off here. If the operator is inside a pool, read its `00-overview.md` first: the concept list, the calibration notes, and the chosen authorship mode all constrain what project is appropriate.
- **`moulinette`** grades the submission. It builds its checklist by lifting the *Mandatory*, *Constraints* and *Bonus* sections straight out of the subject you write, so those three sections are a machine-readable contract, not prose. Keep them itemised and unambiguous.

Do not put a grading rubric or point allocation in the brief. Scoring is the moulinette's, and a subject that pre-announces where the points are teaches people to farm points instead of doing the work. Real subjects never carry one.

## Step 1: Intake

You need enough to close the spec. Gather, conversationally:

1. **Topic and target concepts** — which specific things this project must force the learner to use. If it comes from a pool, take these from the overview rather than re-asking.
2. **Materials** — the docs, handbook, spec, dataset or reference the project should be grounded in. Same rule as `create-pool`: topic-specific content comes from what the operator supplies, never from your own general knowledge of the subject.
3. **Time budget and group size** — a 2-day solo project and a 3-week team project are structurally different documents, not the same document at different lengths. Team projects need the deliverable decomposed into parts that can be worked in parallel behind an agreed interface.
4. **The learner's level** — what they can already be assumed to know, so the brief can lean on it instead of re-explaining it.
5. **Environment constraints** — required tooling, submission format, anything forbidden for reasons outside the pedagogy (no internet, a specific software version, a house style guide).

If the operator hands you material and little else, don't stall — propose concepts from the material (next step) and let the missing details surface as you go.

## Step 2: Propose the project, grounded

Offer **2–3 candidate projects** as one-liners, each naming what it forces the learner to use and roughly how long it takes. Derive them only from the target concepts and the supplied material. Let the operator pick before you write anything long — a full brief for the wrong project is expensive, and the choice is genuinely theirs.

What makes a candidate good:

- **It cannot be completed without the target concept.** If a learner could plausibly finish it by other means, it isn't testing what you think it's testing. This is the single most common failure — a project that *involves* recursion versus one that *requires* it.
- **It has a spine.** One central difficulty everything else hangs off, not five unrelated small tasks. 
- **The difficulty is in the concept, not the plumbing.** If two thirds of the work is parsing a baroque input format, you've written a parsing project.
- **It's grounded.** Say which part of the supplied material it draws on. If nothing in the material supports it, it's not a candidate.

Give each candidate a name and a tagline. Real subjects always have one and it costs nothing to make the thing memorable.

## Step 3: Close the specification

This is the step that separates a subject from a prompt, and it's where most of your thinking should go.

**Pin the input exactly.** Every property a learner could otherwise ask about: format, encoding, ranges, what's guaranteed present, what may be absent, whether it's sorted, what the maximum size is. Say what is guaranteed so they know what they don't have to defend against, and say what isn't so they know they do. BSQ spends five bullets on the input file and is a better subject for it.

**Pin the output exactly.** Byte-exact where the medium allows: exact text, exact ordering, exact separators, exact error stream, exact exit status. "Prints the results" is not a specification.

**Hunt the ambiguities and legislate them.** Walk the spec looking for inputs where more than one output would satisfy it, then rule. Ties, empty input, duplicate keys, rounding, encoding edge cases, degenerate sizes — decide each one in the brief rather than leaving it to be discovered during grading.

### Determinacy in domains that don't naturally have it

Piscine subjects are gradeable because there is exactly one right answer. Most topics can be made to behave this way, and the move is almost always the same: **push determinacy into the input, not into a rubric.** Constrain what the learner is given tightly enough that the correct output becomes a fact.

- *Accounting*: not "prepare a balance sheet" but "here are these 40 journal entries and this opening trial balance; produce the closing trial balance and the P&L." One right answer.
- *Image work*: not "make a nice composition" but "from this source file, produce a 1200×630 export with these five elements at these positions, non-destructively, in a layer structure another editor could pick up." Dimensions, structure and reversibility are all checkable.
- *Analysis / strategy*: not "write a go-to-market plan" but "using only this data pack, produce a plan whose spend totals exactly €250k, where every quantitative claim cites a supplied figure." The arithmetic and the citations are checkable even though the strategy isn't.

Only when a domain genuinely has no determinate output should you fall back to acceptance criteria — and then say so explicitly in the brief, under an *Acceptance criteria* heading rather than *Expected output*, so the moulinette knows not to test for byte-equality. Keep each criterion binary (present/absent, reconciles/doesn't, survives/doesn't) rather than qualitative. "Well structured" is not a criterion; "every figure in the summary table traces to a line in the appendix" is.

## Step 4: Derive the forbidden list

The forbidden list is not hazing and it is not arbitrary. It *is* the pedagogical payload. `my_printf` forbids the entire C library except `malloc`, `free` and `write` because the project is reimplementing the C library — allow `sprintf` and there is no project left.

So derive it from one question: **what shortcut would let someone produce the correct deliverable without touching the concept this project exists to teach?** Ban that. Then stop. Every additional ban past that point converts a project into an obstacle course and costs the learner time on things the project isn't about.

The general form translates cleanly:

| Domain | Concept under test | The ban that protects it |
|---|---|---|
| Systems programming | Manual memory and I/O | The standard library, minus a named few |
| Data work | Understanding the algorithm | The library call that implements it (`sort`, `groupby`, a solver) |
| Accounting | Double-entry mechanics | Spreadsheet auto-sum and pre-built templates |
| Image/tool work | Deliberate technique | One-click filters, presets, generative fill |
| Writing/analysis | Reasoning from evidence | Sources outside the supplied pack |

Choose the shape of the list to fit the ecosystem. **Whitelist** ("the only calls allowed are…") when the permitted set is small and scarcity is the point — it's unambiguous and short. **Blacklist with exceptions** ("the whole standard library is forbidden except…") when the ecosystem is too large to enumerate. Whichever you pick, name specific things. "No helper libraries" is a dispute waiting to happen; "no `pandas`, `numpy` or `itertools`" is a rule.

Also name forbidden *approaches*, not just forbidden tools — hardcoding the expected output, special-casing the example input, copying a total instead of deriving it. These are the ways a submission fakes success, and naming them in the subject is what lets the moulinette score them at zero without an argument.

## Step 5: Write the brief

Use this structure. It's the piscine subject anatomy, generalised past software — adapt the labels to the medium (a `Makefile` becomes a submission format, a binary name becomes a deliverable name), but keep every section, because each one exists to close a specific gap.

```markdown
# <Project Name>
## <tagline>

| | |
|---|---|
| **deliverable** | what is handed in, named exactly |
| **medium** | language, tool, or format |
| **group size** | 1, or 2–4 |
| **duration** | expected working time |
| **submission** | how it is built/opened/run, and where it lives |

> House rules
> - Submit everything needed and nothing else — no build artefacts, no scratch files.
> - Bonus work lives in a separate `bonus/` directory and must not affect the mandatory part.
> - <the domain's equivalent of "errors to stderr, exit 84" — how failure is signalled>

## Context
Two or three sentences on the situation and what the learner will come out knowing.
Give it some personality; subjects people remember get finished.

## Before you start
The concepts and references to read first, pointing at the operator's material.
Man pages, chapters, docs — pointers only, never explanations.

## The task
What must be built, in prose, once. The spine of the project.

## Input
The exact specification from Step 3. What is guaranteed, what is not, what the limits are.

## Expected output
Byte-exact where possible, including ordering, separators, error stream, exit status.
Every ambiguity resolved with an explicit rule.
(Or `## Acceptance criteria` for genuinely non-determinate domains.)

## Constraints
### Authorized
### Forbidden
Tools and approaches, per Step 4.

## Examples
At least one full worked example: exact input, exact output.
At least one edge case — empty, degenerate, malformed.

## Self-check
A short list the learner runs against their own work before calling it done.

## Going further
Bonus work. Only meaningful once the mandatory part is complete.
```

Two sections are worth extra care:

**Examples.** They resolve more ambiguity per line than any amount of prose, and learners read them first. Show the real thing: a terminal transcript, a before/after pair, a filled-in worksheet next to its blank. Include at least one degenerate case, because that's where specs quietly disagree with themselves — and if writing the example reveals that your spec is ambiguous, fix the spec, not the example.

**Self-check.** Every piscine subject builds this in, because there is no instructor in the loop. Make it something the learner can actually run: test cases to write for code, totals that must reconcile for quantitative work, a checklist of properties for a visual or written deliverable. This is also the section the moulinette lifts first, so make it exhaustive rather than indicative.

Never include a solution, a partial solution, a suggested architecture, or a hint that is really an answer. Naming the concepts in *Before you start* is help; sketching the data structure is not. If the operator asks you to add a starting point "just to get them going", say no plainly — it's the same rule `create-pool` and `moulinette` both operate under, for the same reason.

## Step 6: Companion resources

Ship files alongside the brief when it would be unusable without them — an example input file, a source dataset, a starter asset. Some projects ship a test generator so learners can produce their own tests; that's the pattern. Generating a fixture is worth it precisely when producing it by hand would eat time that isn't the point of the project.

Keep them small and out of the way of the learning.

**The answer leaks more easily than you'd expect, and rarely through the front door.** Nobody ships a file called `solution.json` on purpose. What actually happens is subtler, and every one of these has to be checked before the brief goes out:

- A generator that emits expected outputs alongside the inputs it generates.
- A worked example that reaches for a real figure to illustrate something else — a "don't hardcode a total like this" warning whose example total is the actual answer.
- A self-check that states the value to check against ("your totals should come to 26,600") rather than the property to check ("your two totals must agree").
- Input data whose derived figures are recoverable from a subtotal that didn't need to be there.
- A resource filename or a comment that names the result.

Treat any number, string or structure that a learner is supposed to *produce* as radioactive everywhere in the package, not just in `resources/`. The rule is a property of the whole deliverable: if a figure appears anywhere the learner can read, it is no longer something they have to derive. When the project has a computed answer, grep the finished package for it before shipping — this is the cheapest check available and it catches the illustrative-example case, which is the one that gets through.

## Output

```
<project-slug>/
├── subject.md
└── resources/          # only when the brief needs them
    ├── example_input
    └── generate_input.py
```

When invoked inside a pool, place the directory in the pool alongside the days it follows (`rust-pool/project-01-<slug>/`), and add a line to the pool's `00-overview.md` so the arc stays legible.

## Before you ship it

Read the brief back as the learner, then as the grader. Two questions:

1. **Could I produce a correct deliverable that the brief didn't anticipate?** If yes, there's an unlegislated ambiguity — find it and rule on it.
2. **Could I satisfy every stated requirement without using the target concept?** If yes, the forbidden list has a hole.
3. **Is any part of the answer already in the package?** Grep for it if it's a figure; reread the examples and the self-check if it isn't. See *Step 6*.

Then hand it over and ask whether the difficulty and duration look right. Adjusting scope before anyone starts is cheap; discovering on day four that the project was a week's work is not. Once they're happy, you're done — grading it is the moulinette's job, and if they get stuck partway through, that's the project working as intended.
