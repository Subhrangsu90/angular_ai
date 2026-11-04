# ai-cli

Built in week 3. One command; switch provider and model with a flag (`--provider ollama --model qwen`).

## Planned structure

```
src/
  index.ts              # CLI entry, flag parsing
  config.ts             # provider + model from flags / env
  providers/
    provider.ts         # shared interface: chat(), stream()
    hosted.ts           # Claude / Gemini / OpenAI SDK
    ollama.ts           # local models via Ollama HTTP API
  utils/
    tokens.ts           # token counting + cost estimate
.env.example
package.json
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
