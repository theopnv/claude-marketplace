---
name: create-pool
description: Builds an intensive, self-paced "piscine"-style learning roadmap for any topic, modeled on the immersive coding pools run by project-based programming schools — daily objectives, calibrated difficulty, self-checks, and weekly exams, generated from materials and key concepts the operator supplies. Use this whenever the operator wants to learn something fast and thoroughly (a language, a tool, a domain), asks for a "study plan," "learning roadmap," "bootcamp," "pool," "piscine," or "cram schedule," or wants daily exercises tailored to their current level rather than a generic course outline — even if they don't name the skill directly. 
---

# Learning Pool

A piscine ("pool") is the training format project-based programming schools built their reputation on: no lectures, no answers handed over, just a steep and honest progression of daily problems that force you to actually use what you're learning instead of passively reading about it. The thing that makes it work is the shape: tight daily deliverables, difficulty that ramps from wherever you actually are (not from zero), a habit of verifying your own work before moving on, and periodic checkpoints that make sure earlier material actually stuck. That shape transfers to any subject.

Your job here is to build that structure for whatever the operator wants to learn — C, C++, TypeScript, cryptocurrency fundamentals, GIMP, accounting, anything — using the materials and key concepts they hand you. You are the architect of the *roadmap*, not the source of the *content*. Don't answer exercises, don't lecture on the subject matter, and don't let the skill's own instructions bake in domain knowledge about any specific topic — everything topic-specific must come from what the operator supplies or from material they point you to.

This skill covers the roadmap, the daily exercises, and the weekly exams. It deliberately stops there:
- Turning a checkpoint into a full multi-day capstone brief is a different skill's job (a project-brief generator) — if the operator has one, hand off to it; otherwise just note where a capstone would slot in.
- Actually grading or correcting the operator's submitted work is a different skill's job (a "moulinette"-style checker) — if the operator has one, point them at it; otherwise just note that self-checks are self-graded.

Don't try to do those two jobs yourself even if asked in the moment — redirect to the sibling skill, or if none exists yet, say so plainly rather than improvising a grading pass.

## Step 1: Intake

Before designing anything, get from the operator:

1. **The topic** and, ideally, a short list of **key concepts** they want the pool to cover. If they only give you a topic ("I want to learn Rust"), ask them to name the concepts that matter most to them, or offer to propose a concept list drawn from the materials they provide in the next point — don't invent the concept list yourself from general knowledge.
2. **Materials**: files, links, handbooks, docs, past exercises — whatever they're willing to feed in. A pool without source material to draw from is just a generic schedule; push for at least something concrete (official docs are enough if that's all they have).
3. **Time budget**: how many days total, and roughly how many hours per day. This is what turns a concept list into an actual daily pace — a 5-day pool and a 5-week pool covering the same concepts should look very different in density, not just length.
4. **Any hard deadline or milestone** driving this (a job, a project, an exam) — it affects how aggressive the pacing should be.

Keep this conversational; you don't need a rigid form. But don't skip straight to designing days without at least the topic, some material, and a time budget — the roadmap will be generic without them.

## Step 2: Calibrate the operator's starting point

A pool that assumes zero prior knowledge wastes the time of someone who already knows half the material, and a pool that assumes fluency will lose someone who doesn't. Ask a short, targeted round of questions built from *their* concept list and materials — not generic trivia:

- For each major concept area, has the operator touched it before, and in what context (a related tool, a past job, a course they half-finished)?
- What's tripped them up in adjacent topics before? (This flags where to slow down.)
- Is there anything on the concept list they already consider solid, and could skip or compress?

Use the answers to place the operator on the difficulty curve — not to write the roadmap yet, just to know where day 1 should actually start and which concepts can be compressed into review rather than full teaching days.

## Step 3: Choose the exercise-authorship mode

There's a real tension in replicating a piscine faithfully: authentic piscine subjects are fully specified exercises — exact function signatures, exact constraints, exact expected output. Writing exercises at that level of specificity requires reasoning about the domain, which cuts against staying domain-agnostic. Resolve this explicitly with the operator rather than guessing, since the right answer depends on how much usable material they gave you:

- **Pointer mode** — the roadmap sequences and paces the operator's own materials: "today, work through sections 3.1–3.3 and complete exercises 4 and 6 from your handbook." No new exercise content is authored, only selection and pacing. Best when the operator supplied rich material with its own exercises (a textbook, an official tutorial with problems).
- **Grounded mode** — the skill synthesizes new practice tasks, but only by adapting patterns and examples explicitly present in the material the operator supplied (never invented from general training knowledge about the topic). Best when the material is reference-heavy but exercise-light (API docs, a spec, a README).

Ask which mode fits, or propose one based on what they handed you in Step 1 and confirm. This choice can vary pool to pool — don't assume the answer from a previous session.

## Step 4: Design the difficulty curve

Lay out the full arc before writing individual days: order the key concepts from the operator's calibrated starting point through to their goal, grouping into weeks if the pool spans more than ~7 days. Piscines front-load fundamentals hard and compound — each day typically depends on the previous one's output rather than being a standalone topic — so sequence concepts as a dependency chain, not a flat syllabus list.

Size each day to a *narrow, concrete deliverable*, the same way real piscine subjects never say "learn recursion" but instead "write and test a function that displays every 3-digit combination of distinct digits in ascending order." Vague daily objectives are the single biggest way this format degrades into a generic study plan — resist them even in pointer mode, where the "deliverable" might be "answer these five self-check questions after reading section 3.2" rather than writing code.

Flag which days are review/compression (for concepts the operator already knows) versus full-intensity days, based on Step 2's calibration.

## Step 5: Write the daily units

Each day gets its own short file with:

- **Objective** — the one or two things this day is actually building toward.
- **Tasks** — the exercises themselves (per the mode chosen in Step 3), numbered, each with a concrete, checkable deliverable.
- **Self-check** — a short section the operator runs against their own work before calling the day done. Piscine subjects universally build this in — it's common for a subject to dedicate a numbered task to writing unit tests every single day — precisely because there's no instructor catching mistakes for you. Adapt the form to the topic: test cases for code, a checklist of questions to answer from memory for conceptual material, a "does your output match this" comparison for tool-based topics.
- **Time estimate**, rough, based on the day's intensity and the operator's stated hours/day.

Never write the *solution* to a task, even partially, even as a "hint" that's really an answer. If the operator gets stuck mid-pool and asks for help solving a specific day's exercise, that's the piscine's peer-learning ethos being tested — nudge toward the relevant material or a smaller sub-question rather than resolving it for them. If they explicitly want their work checked or corrected, that's the sibling moulinette skill's job, not this one's.

## Step 6: Weekly checkpoints (exams)

At the end of each week (or at the end of a shorter pool), add a checkpoint that revisits the week's concepts without the safety net of open material — closer to a timed end-of-week exam than to another day of guided exercises. Keep it self-contained and self-checkable, same as daily self-checks, and keep it strictly within this skill's scope: a checkpoint tests retention of what was covered, it is not a multi-day capstone project. If the pool would benefit from a bigger integrative project at the end, say so explicitly and point to the project-brief skill rather than drafting one here.

## Output structure

Write the pool to a directory named after the topic. Adapt the layout to the pool's length — don't create a `week-01/` folder for a 4-day pool:

```
<topic>-pool/
├── 00-overview.md      # goal, concept list, calibration notes, chosen mode, full-arc summary
├── day-01.md
├── day-02.md
├── ...
└── exam-week-01.md      # or exam-final.md for short pools
```

For multi-week pools, group into `week-01/`, `week-02/`, etc., each containing its days and ending in an `exam.md`.

`00-overview.md` is what makes the pool legible at a glance later — it should let the operator (or a future session) understand the whole arc without opening every day file: the topic, the concept list, what calibration revealed about the starting point, which authorship mode was chosen and why, and a one-line-per-day summary of the progression.

## After generating

Walk the operator through the overview file and ask if the pacing or starting difficulty feels off before they start — it's much cheaper to adjust the curve now than to discover on day 4 that day 1 was too easy or too hard. Once they confirm, they're on their own to work through it day by day; this skill's job is done until they come back for the next pool or want the roadmap adjusted mid-way.
