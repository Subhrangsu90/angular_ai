# Chat with your docs

Built in week 9. Upload PDF or markdown, ask questions, get answers with sources.

## Planned structure

```
server/
  src/
    ingest/
      parse.ts              # PDF / markdown -> text
      chunk.ts              # size + overlap
      embed.ts              # hosted or Ollama embeddings
    db/
      schema.sql            # pgvector table + index
      vector-store.ts       # insert, top-k query
    rag/
      retrieve.ts
      prompt.ts             # chunks -> prompt with citation markers
    routes/
      upload.ts
      ask.ts                # SSE answer + sources
client/
  src/app/features/docs-chat/
    upload.component.ts
    ask.component.ts
    source-list.component.ts
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
