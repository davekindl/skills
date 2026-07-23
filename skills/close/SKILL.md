---
name: close
description: "Use when you say /close, 'close the session', 'wrap up', or want the end-of-session ritual: achievements + unfinished-TODO summaries, durable state written to disk, work checkpoint-committed. Also use before a planned context compaction or when the context window is filling up."
---

# /close — Session Close-Out Ritual

## Overview

One command that ends an AI working session cleanly: two structured summaries
(achievements, unfinished TODOs), durable state written to disk, and a
checkpoint commit. The session's value must survive the session.

**Core principle: nothing important may live only in the chat.** If it isn't
in a state file or a commit, it didn't happen. Chat history gets compacted,
sessions end, context windows overflow — disk and git are the only memory
that persists.

## Steps

1. **Gather evidence — don't summarize from memory alone.**
   - `git log --oneline -15` + `git status --short` on the active project(s).
     The commits made this session are the achievement skeleton.
   - Scan the session for: decisions the operator made, agent runs and their
     verdicts, files created, and — critically — what was *verified* (tests
     passed, gates run, output inspected) versus what was merely produced.

2. **Write the ACHIEVEMENTS summary (~500–1000 words, in chat).**
   - Lead with the headline outcome, not chronology.
   - Anchor every claim to an artifact: commit hash, file path, test result,
     measured number.
   - Keep verified work separate from unverified work — a claim without a
     check is a hope, not an achievement.
   - Record decisions made and their rationale. The WHY survives; the
     chatter doesn't.

3. **Write the UNFINISHED TODOs summary (~500–1000 words, in chat).**
   Split into: (a) blocked on the operator — name exactly what input is
   needed; (b) next planned work, with effort estimates; (c) items carried
   from earlier sessions still open; (d) verifications still pending.
   For each item: where the spec lives on disk, so a fresh session can
   execute without this conversation.

4. **Update your backlog file** (e.g. `BACKLOG.md` in the repo root).
   One new entry per open work item — condensed and pointer-rich, NOT the
   1000-word prose. Backlog entries point to spec files; they don't
   duplicate them.

5. **Update `session-state.md`** (keep it wherever your project keeps
   working notes; gitignore it if it contains half-formed thinking).
   PREPEND a new session block — prior blocks are history, never delete
   them. Each block records: branch + commits, Completed, Blocked,
   Next Steps, and **Failed Approaches (DO NOT RETRY)** with this session's
   new dead ends.

6. **Checkpoint commit** anything the operator has ratified (current branch
   only — NEVER push without explicit confirmation). Skip files still
   awaiting a decision, and say so in the summary instead.
   - Commit tracked work only — never `git add` gitignored paths. If your
     state files are gitignored, the disk save IS the deliverable; they
     don't need a commit to count.

7. **Optional, ask once:** anything worth adding to a lessons-learned file
   (what worked / what didn't)? Append only if the operator engages — don't
   block the close on it.

## Quick Reference

| Artifact | Gets |
|---|---|
| Chat | 2 structured summaries (achievements, TODOs) |
| Backlog file | One condensed entry per open item, pointer-rich |
| session-state.md | Prepended block incl. Failed Approaches |
| git | Checkpoint commit of ratified work |

## Common Mistakes

- **Summarizing from vibes instead of `git log`** — achievements drift from
  reality. Anchor to commits.
- **Pasting prose into the backlog** — the backlog is a scan-once queue;
  long prose belongs in spec files it points to.
- **Overwriting session-state.md** — always prepend; prior blocks are the
  cross-session memory.
- **Forgetting Failed Approaches** — the most valuable section; a fresh
  session WILL retry the same dead ends without it.
- **Committing unratified work** — files pending a decision stay
  uncommitted; note them in the summary instead.
