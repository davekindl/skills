---
name: open
description: "Use when you say /open, 'open the session', 'resume where we left off', 'session start ritual', 'what were we doing', or 'pick up where we left off' at the start of an AI working session. The resume counterpart of /close."
---

# /open — Session Resume Ritual

## Overview

One command that starts an AI working session oriented: read the durable state
`/close` left behind, check git reality, present a compact picture, and ask
which thread to pick up. It's a ritual, not an essay — the whole output should
fit on one screen.

## Steps

1. **Read your session-state file** if it exists — the TOP block only (blocks
   are prepended newest-first). Pull: Completed, In Progress, Blocked, Next
   Steps, Failed Approaches. Common locations: `session-state.md` in the repo
   root, `.notes/session-state.md`, or wherever `/close` writes it in this
   project. If you keep a separate git-state snapshot file, read that too.

2. **Check the last export/log** if your `/close` produces one — list the newest
   file in your exports directory (sort by modified time). Mention its name and
   offer to read its tail for context; do NOT read the whole thing unprompted —
   exports can be large.

3. **Check git reality:** `git status --short` + `git branch --show-current` in
   the working directory. State files describe the LAST session; git describes
   NOW — flag any mismatch out loud (e.g. "state file says X was committed, but
   git shows it uncommitted").

4. **Output a compact orientation, then ask.** Format:

   ```
   ## Session Open — <date>
   - Branch: <branch> | Uncommitted: <N> files
   - Last session (<date from state file>): <one-line headline>
   - DONE: <2-3 bullets max>
   - IN PROGRESS: <where work stopped, be specific>
   - BLOCKED: <what's waiting on you, or "nothing">
   - Next steps on record: <numbered, from state file>
   ```

   Then ask which thread to pick up — offer the recorded next steps as options
   plus "something else".

## Rules

- **Short.** No 1000-word recaps at open — that's what `/close` wrote to disk
  for. Orientation only.
- **Never retry Failed Approaches** from the state file without acknowledging
  the prior failure out loud.
- If NO state files exist, say so in one line and fall back to
  `git log --oneline -10` + `git status` for orientation.
- Missing files are normal in a fresh project — degrade gracefully, never error
  out.

## Common Mistakes

- **Reading every block of the session-state file** — only the top (newest)
  block matters at open; the rest is history.
- **Bulk-reading the newest export** — offer its tail; read fully only if asked.
- **Skipping the git check** — state files can be stale; git is the ground truth
  for "now".

## Pairs with /close

`/open` reads what `/close` wrote. If you don't run `/close` at the end of a
session, `/open` has nothing durable to resume from and will fall back to git
history. The two are a set — install both.
