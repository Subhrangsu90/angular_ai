# Voice laptop controller

Built in week 18. Whisper + tool-calling local model + MCP tools in a voice command loop.

## Planned structure

```
src/
  listen.ts               # mic -> Whisper -> text
  intent.ts               # local model picks an MCP tool
  mcp-client.ts           # calls project-laptop-mcp-server
  confirm.ts              # human approval for risky actions
  loop.ts
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
