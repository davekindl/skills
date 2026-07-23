# Reference: EU AI Act — Article 50 Transparency Obligations

Background for AI-disclosure clauses and the self-assessment checklist. Not loaded during generation. Not legal advice. Source: Regulation (EU) 2024/1689 (the "AI Act").

## Why this matters for you
your consultancy is mostly a **deployer** (and sometimes provider) of limited-/minimal-risk AI (content generation, image/video/voice). The binding obligation that touches almost every deliverable is **Article 50 transparency**. Most of his systems are not high-risk, but transparency still applies.

## Article 50 — the four core duties
1. **50(1) — AI systems that interact with people.** Providers must design systems so that users are informed they are interacting with an AI, unless it is obvious from the context. → A client-facing chatbot must say it's AI.
2. **50(2) — Synthetic content marking.** Providers of generative AI must ensure outputs (audio, image, video, text) are **marked in a machine-readable format** and detectable as artificially generated/manipulated, where technically feasible. → Affects AI media pipelines.
3. **50(4) first subpara — Deepfakes.** Deployers who generate or manipulate image/audio/video constituting a **deep fake** must **disclose** that the content is artificially generated or manipulated. → ElevenLabs voice + Seedance video outputs.
4. **50(4) second subpara — AI-generated text on matters of public interest.** Deployers who use AI to generate or manipulate **text published to inform the public on matters of public interest** must disclose it is AI-generated (unless human review/editorial responsibility exists). → Affects AI-written public content.

## Risk tiers (context for Step 2 of the self-assessment)
- **Prohibited (Art.5):** social scoring, untargeted facial-recognition scraping, certain biometric categorisation, manipulative/exploitative systems → must not be used.
- **High-risk (Art.6 + Annex III):** e.g. AI in employment/HR decisions, credit scoring, education assessment, critical infrastructure → conformity assessment, risk management, documentation.
- **Limited-risk:** chatbots, deepfakes, emotion recognition → Article 50 transparency.
- **Minimal-risk:** spam filters, most content generation → no specific obligations beyond voluntary good practice.

## Practical compliance for the toolkit
- Every AI-generated client deliverable carries an **AI-generation disclosure footer** (see `templates/ai-output-disclaimer.md` and `clauses/ai-accuracy-disclaimer.md`).
- Deepfake/voice/video outputs get an **explicit "artificially generated" label**.
- The quarterly **self-assessment** (`checklists/eu-ai-act-self-assessment.md`) records the inventory, risk classification, and transparency status.

## Timing
The AI Act entered into force in 2024 with **staggered application dates**; Article 50 transparency obligations apply from a later date than the prohibitions. [REVIEW] Confirm the exact applicability date for transparency duties at the time of use, as the phased timeline is fixed in the Regulation.

> For orientation only. Read the official text and Commission guidance/codes of practice. Have a lawyer confirm classification of any specific AI system, especially anything near the high-risk Annex III list.
