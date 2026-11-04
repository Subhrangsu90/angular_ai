# AI chat app (Angular + Express)

Built in week 4–7. Streaming chat with model switcher, history, system-prompt editor, and editor AI commands.

## Planned structure

```
server/                     # week 4
  src/
    index.ts                # Express app
    routes/chat.ts          # POST /api/chat -> SSE stream
    providers/              # hosted + ollama adapters
    middleware/rate-limit.ts
client/                     # weeks 5–7 (ng new client)
  src/app/
    core/
      chat-stream.service.ts    # fetch + ReadableStream -> signal
      conversation.store.ts     # history (localStorage, then Postgres)
    features/chat/
      chat-page.component.ts
      message-list.component.ts
      message-input.component.ts
      markdown-message.component.ts
    features/settings/
      model-picker.component.ts
      system-prompt-editor.component.ts
    features/editor/            # week 7, ProseMirror slash commands
      ai-slash-commands.ts
      ai-suggestion.plugin.ts
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
