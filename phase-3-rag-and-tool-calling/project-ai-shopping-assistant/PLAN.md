# AI shopping assistant

Built in week 10–11. Tool-calling assistant over your product API, plus natural-language product search and admin description generator.

## Planned structure

```
server/
  src/
    tools/
      search-products.ts
      get-order-status.ts
      get-weather.ts
      registry.ts           # tool schemas the model sees
    agent/tool-loop.ts      # model -> tool call -> result -> model
    search/semantic-product-search.ts   # pgvector
    admin/generate-description.ts
client/
  src/app/features/assistant/
    assistant-chat.component.ts
    tool-call-card.component.ts   # "Searching products…"
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
