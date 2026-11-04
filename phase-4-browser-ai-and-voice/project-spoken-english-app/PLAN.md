# Spoken-English practice PWA

Built in week 14–15. Pick a work scenario, speak, get grammar fixes, better phrasing, a 1–10 score, WPM and filler-word count.

## Planned structure

```
src/app/
  core/
    speech-to-text.service.ts     # Web Speech API / Whisper
    text-to-speech.service.ts     # speechSynthesis
    recorder.service.ts           # mic permissions + states
    feedback.service.ts           # model -> JSON feedback (Zod-validated)
    session.store.ts              # saved sessions, progress
  features/
    topics/topic-list.component.ts      # standup, code review, interview
    practice/practice.component.ts
    feedback/feedback.component.ts
    progress/progress-chart.component.ts
  workers/
    whisper.worker.ts
ngsw-config.json                  # PWA
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
