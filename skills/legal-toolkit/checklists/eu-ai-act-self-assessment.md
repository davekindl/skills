# EU AI Act Self-Assessment Checklist

Run quarterly. Last run: [DATE]

## Step 1: AI System Inventory

List every AI system in use:

| System | Provider | Purpose | Risk Level | Transparency Done? |
|--------|----------|---------|-----------|-------------------|
| Claude (API) | Anthropic | Content generation, coding, analysis | Minimal | [ ] |
| GPT-Image-2 (kie.ai) | OpenAI/kie.ai | Image generation | Minimal | [ ] |
| ElevenLabs | ElevenLabs | TTS, voice cloning | Limited (deepfake risk) | [ ] |
| Deepgram Nova-3 | Deepgram | Transcription | Minimal | [ ] |
| Seedance 2.0 | ByteDance/kie.ai | Video generation | Limited (deepfake risk) | [ ] |

## Step 2: Risk Classification

For each system, classify:
- [ ] **Prohibited** (social scoring, real-time biometric in public, manipulation) → STOP using immediately
- [ ] **High-risk** (HR decisions, credit scoring, education assessment, law enforcement) → Full conformity assessment required
- [ ] **Limited-risk** (chatbots, deepfakes, emotion recognition) → Transparency obligations
- [ ] **Minimal-risk** (spam filters, content generation, search) → No specific obligations beyond general transparency

## Step 3: Transparency Obligations (Article 50)

- [ ] All AI-generated content delivered to clients is labeled as AI-generated
- [ ] Any system that interacts with humans discloses it is AI
- [ ] Deepfake content (AI-generated video/audio/images of real people) is clearly labeled
- [ ] AI-generated text published as if human-authored is disclosed

## Step 4: Documentation

- [ ] Technical documentation maintained for each AI system
- [ ] Data sources and processing purposes documented
- [ ] Human oversight points identified for each workflow
- [ ] Incident log maintained (any AI system failure or unexpected output)

## Step 5: Sub-Processor Compliance

- [ ] Each AI provider has a valid DPA in place
- [ ] EU-US data transfer mechanism verified (Data Privacy Framework or SCCs)
- [ ] Sub-processor list is current and clients are informed of changes

## Step 6: Training

- [ ] You (and any future employees) trained on AI Act obligations
- [ ] Clients informed of AI usage in their projects

## Result

| Category | Status |
|----------|--------|
| Prohibited AI | None in use ✓ |
| High-risk AI | None in use ✓ / Action needed |
| Transparency | Compliant ✓ / Gaps: [list] |
| Documentation | Complete ✓ / Missing: [list] |
| Sub-processors | Compliant ✓ / Gaps: [list] |

Next assessment due: [DATE + 3 months]
