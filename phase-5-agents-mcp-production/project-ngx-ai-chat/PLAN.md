# ngx-ai-chat (npm library)

Built in week 20. Your best components extracted into a signal-based, provider-agnostic Angular library with docs and a demo site.

## Planned structure

```
projects/
  ngx-ai-chat/            # ng generate library ngx-ai-chat
    src/lib/
      components/
        chat.component.ts
        message-list.component.ts
        markdown.component.ts
      services/
        ai-stream.service.ts
      adapters/
        ai-adapter.ts       # interface
        hosted.adapter.ts
        ollama.adapter.ts
        in-browser.adapter.ts
      provide-ai-chat.ts
    src/public-api.ts
  demo/                   # docs + demo site
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
