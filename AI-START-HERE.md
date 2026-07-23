# AI-START-HERE — davekindl / skills

> **Human?** This file is for your AI assistant. Point Claude Code, Codex, or any
> capable agent at this repo and say *"read AI-START-HERE.md and integrate these
> skills into my setup."* It installs them and interviews you to customize the
> ones that need it.

---

## FOR THE AI AGENT READING THIS

You've been pointed at **davekindl's public skill library** (30 skills, free).
Your job: install the skills the user wants into their environment, and
**customize the ones that need per-user context by interviewing the user** — do
not guess their niche, projects, or config, and never invent credentials.

Work the four steps in order. Narrate what you're doing; ask before writing
outside this folder.

### Step 1 — Inventory (read, don't act yet)

- `skills/` — 30 self-contained skills, each a `SKILL.md` (+ scripts/references).
- `README.md` — the human-facing catalog, grouped by topic.
- This file — your playbook.

Ask the user: **all 30, or a subset?** Most people want a few. Offer the
README's groupings so they can pick by topic.

### Step 2 — Install

Per the user's agent:

- **Claude Code:** copy each chosen `skills/<name>/` into `~/.claude/skills/<name>/`
  (global) or `<project>/.claude/skills/<name>/` (project-scoped). Live next
  session — verify against the agent's skill list.
- **Codex / other:** load `skills/<name>/SKILL.md` as instructions at session
  start, or when the task arises. Scripts/references are called by path.

Confirm each install before moving on.

### Step 3 — Customize (interview the user — the important part)

Most skills are **runtime-interactive**: they ask for what they need when you run
them (e.g. `animated-website` asks for the video + brand; `gpt-image-2-techniques`
runs a discovery step and ships only a generic `acme-consulting` brand kit you
copy for your own). Nothing to configure up front.

A few need to know something about **this user** before they're useful. For each
one the user installed, offer **two paths** and let them choose:

> **A) Scan & infer** — "Point me at your repo(s)/project(s) and I'll read them to
> propose the config, then confirm each value with you."
>
> **B) Answer a few questions** — "I'll ask you N short questions."

**Always confirm the final config before writing it.** Store it in the skill's
own config location or the user's project config — **never** back into the
public `SKILL.md`.

#### Skills that need an interview

| Skill | What it needs to know |
|---|---|
| `product-evolver` | Target project + what "better" means (rank: bugs / UX / competitive gaps / new ideas) + target user + no-touch constraints + run cadence |
| `business-evolution-audit` | Whose sites to audit (your niche/market), your competitor set, your service offering + rate, your outreach identity |
| `octopus` | Your project ecosystem (which repos/projects), your research niche(s), what to evolve if anything, which API integrations you have (image/search/Slack), your morning-brief preferences |
| `megaplan` | The specific architectural decision + its constraints (asked at run time, but confirm the project context first) |
| `niche-skill-forge` | The domain to research + your sources/preferences |
| `polish-orchestrator` | Target project root + which of the 15 audit modes matter to you + your hook-wiring paths (see its own SKILL.md) |
| `firecrawl` | Your Firecrawl API key (set as env var — never commit it) |

#### Skills that need a secret (not an interview, just a key)

Some skills call paid APIs. They read keys from **your** environment/config —
never hardcode or commit them. Set them as env vars before first run:

- `gpt-image-2-techniques` → `KIE_AI_API_KEY` (kie.ai)
- `firecrawl`, `business-evolution-audit` → `FIRECRAWL_KEY`
- Any video/audio skill → its provider's key per its SKILL.md

If a key isn't set, tell the user which env var to set — don't proceed blind.

#### Example — the `octopus` interview

`octopus` is a nightly autonomous operations system; it's useless without knowing
what it operates ON.

- **Scan path:** "Point me at your projects directory. I'll read each repo's
  README + recent git activity and propose: which projects to include, their
  apparent focus, and which arms (evolve / research / outreach / content) fit.
  Then confirm."
- **Manual path — ask:**
  1. Which projects/repos should it run over? (paths)
  2. Your research niche(s)? (what should the signal-scan track)
  3. Anything to actively evolve/improve, or sense-and-report only?
  4. Which integrations do you have? (image gen, web search, Slack, calendar)
  5. What do you want in the morning brief?

Write answers to the skill's config; echo them back for correction before the
first run.

### Step 4 — Integrate & report

- Note how the installed skills compose with what the user already has (CI,
  design system, existing agents) — slot in, don't duplicate.
- One-screen summary: installed / customized / ready-to-run / the single best
  first command to try.

---

## A note on placeholders

These skills are shipped **de-personalized**. Any `[Your Name]`, `[Your Brand]`,
`acme-consulting`, `<projects-root>`, or example niche is a **placeholder** to
replace with the user's real values via the interview above — never a real
credential, and never something to carry into a live run as-is.

---

davekindl · NOTREPLACED
