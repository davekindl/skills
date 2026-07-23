---
name: course-creator
description: "Turn expertise into structured online courses. Backward design from transformation goal, Bloom's taxonomy progression, HOOK-TEACH-DO-CHECK lesson anatomy, assessment generation, multi-format export (HTML modules, Markdown, SCORM 1.2). Trigger on: 'create a course', 'build a course', 'course about', 'teach [topic]', 'lesson plan', 'curriculum for', 'online course', 'package as course', 'training module', 'workshop content', 'course creator', 'SCORM export'. Also triggers when you mention packaging your methodology, your framework content, or your long-form content as educational products."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, WebSearch
---

# COURSE CREATOR

> Expertise -> transformation contract -> Bloom's progression -> HOOK-TEACH-DO-CHECK lessons -> assessments -> packaged course. Every lesson earns the next.

## Pedagogical Backbone

**Bloom's Ladder** enforces cognitive progression across modules:

| Module | Bloom's Level | Learner Does | Assessment Type |
|--------|--------------|-------------|-----------------|
| 1 | Remember | Recall terms, recognize patterns | Quizzes, matching |
| 2 | Understand | Explain concepts in own words | Summarize, compare |
| 3 | Apply | Use knowledge in guided exercises | Scenario exercises |
| 4 | Analyze | Break down problems, evaluate tradeoffs | Case study breakdowns |
| 5 | Evaluate/Create | Judge, critique, design solutions | Peer review + rubric |
| 6 | Create | Build the real thing | Capstone project |

## 6-Phase Workflow

### Phase 1: Discovery (5-10 questions)
- What transformation do learners achieve? ("After this course, you can ___")
- Who is the learner? (skill level, role, constraints)
- How long? (micro 1-2h, standard 4-8h, deep-dive 10-20h)
- Format? (self-paced, cohort-based, hybrid)
- Your unique angle? (what YOU know that Google doesn't)
- Platform? (determines export format constraints)
- Capstone/certification needed?

Output: `course-brief.md`

### Phase 2: Architecture (automated)
- Generate module structure mapped to Bloom's levels
- Define learning objectives per module (verb + measurable outcome)
- Bloom's verb bank: define/list/recall → explain/compare → implement/solve → distinguish/classify → judge/argue → design/produce
- Specify assessment types per module
- Map prerequisite dependencies
- Estimate time per lesson
- Tag content volatility (stable/evolving/volatile)

Output: `course-outline.md` -- **you review before Phase 3**

### Phase 3: Content Generation (per-module, iterative)
Generate lessons following **HOOK-TEACH-DO-CHECK** anatomy:

1. **HOOK** (30 sec): Why this matters right now -- provocative question, failure story, surprising stat, or "what would you do" scenario
2. **TEACH** (3-7 min): Core concept with examples. Max passive consumption: 5 min before interaction.
3. **DO** (5-15 min): Active exercise, template, or build task
4. **CHECK** (2-3 min): Self-assessment or reflection prompt

Mark `[CREATOR: your example/story here]` where your personal experience is required. AI handles structure; you provide substance.

Output: `modules/NN-slug/` directory per module

### Phase 4: Assessment Pack (automated)
- Per-lesson micro-quizzes
- Per-module knowledge checks
- Cumulative mid-course assessment
- Final exam or capstone rubric
- Spaced repetition review prompts (key concepts resurface in later modules)

Output: `assessments/` directory

### Phase 5: Packaging (format-specific)
Export options:
- **HTML modules:** self-contained pages with embedded JS quizzes, nav, progress tracking via localStorage
- **Markdown curriculum:** clean .md files for Teachable/Kajabi/Notion import
- **SCORM 1.2 package:** imsmanifest.xml + HTML content, widest LMS compatibility
- **Standalone site:** single HTML file, all modules, localStorage progress

Output: `exports/` directory

**SCORM packaging (do not hand-roll the manifest):** export the HTML lessons,
then package them with any standard SCORM 1.2 packager or your LMS's import
tool. The finished zip needs a schema-valid `imsmanifest.xml` at its root and
lessons that report `cmi.core.lesson_status=completed` via the SCORM runtime
API — mainstream packagers handle both. Verify the package imports cleanly
into the target LMS (Moodle/Canvas/TalentLMS/SCORM Cloud) before shipping.

### Phase 6: Quality Audit (automated)
- Every lesson has: learning objective, assessment, active element
- Bloom's progression is monotonically increasing
- No lesson exceeds time estimate
- All `[CREATOR:]` markers addressed
- Heading hierarchy correct
- Links and references valid

Output: `course-quality-report.md`

## Anti-Patterns (8 things the skill prevents)

1. **Knowledge dump:** Cramming everything into one course. Enforce single transformation goal.
2. **Missing validation:** Building full course before confirming demand. Phase 2 outline IS the validation artifact.
3. **Assessment amnesia:** Every lesson gets at least one check. No exceptions.
4. **Passive video walls:** Mandatory active element within every lesson. Max 5 min passive.
5. **Flat difficulty:** Bloom's progression is enforced. Early = Remember/Understand, late = Create.
6. **Missing context bridge:** Every concept lesson gets a companion "in practice" element.
7. **Monolithic lessons:** Flag and auto-split any lesson exceeding 10 min.
8. **Generic AI filler:** Mark `[CREATOR:]` insertion points. AI structures, human provides substance.

## File Structure

```
course-{slug}/
├── course-brief.md
├── course-outline.md
├── course-quality-report.md
├── modules/
│   ├── 01-{slug}/
│   │   ├── README.md           (module overview, objectives, time)
│   │   ├── lesson-01.md        (HOOK-TEACH-DO-CHECK)
│   │   ├── lesson-02.md
│   │   ├── quiz.md             (module knowledge check)
│   │   ├── exercise.md         (hands-on with rubric)
│   │   └── resources/
│   │       ├── cheatsheet.md
│   │       └── template.md
│   └── 02-{slug}/
├── assessments/
│   ├── midpoint-check.md
│   ├── final-exam.md
│   └── review-prompts.md
└── exports/
    ├── html/
    ├── markdown/
    └── scorm/
```

## Tool Integration

| Phase | Tool | Purpose |
|-------|------|---------|
| 1 | AskUserQuestion | Structured discovery |
| 2 | Write | course-outline.md |
| 3 | Write, WebSearch | Lesson content, current data/examples |
| 4 | Write | Assessment generation |
| 5-HTML | Write | Self-contained HTML with embedded quiz JS |
| 5-SCORM | Write | HTML lessons -> package with any SCORM 1.2 packager (imsmanifest.xml at zip root) |
| 6 | Read, Grep | Quality audit checks |
