# claude-marketplace

A marketplace of Claude Code plugins. No guarantee they work or are safe to use — try at your own risk.

## Install

```
/plugin marketplace add theopnv/claude-marketplace
/plugin install fortytwo@plugins-from-theopnv
```

## Plugins

### fortytwo

Skills for running a project-based, piscine-style learning workflow — the format used by these famous french programming schools.

- **create-pool** — builds a self-paced learning roadmap (a "piscine") for any topic: daily objectives, difficulty ramped from the operator's actual level, self-checks, and weekly exams, all generated from material the operator supplies.
- **create-project** — writes a fully-specified project brief for a pool checkpoint or standalone assignment: exact input/output, forbidden tools and approaches, worked examples, and a self-check.
- **moulinette** — grades a submission against its brief: runs/opens/recomputes the work, scores it 0–20 with an evidence-backed breakdown, and reports where points were lost — without handing over the fix.

The three hand off to each other (roadmap → brief → grade) but each also works standalone.
