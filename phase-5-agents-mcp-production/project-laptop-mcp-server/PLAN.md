# Laptop MCP server

Built in week 17. MCP server in TypeScript exposing tools: open app, open VS Code folder, git push.

## Planned structure

```
src/
  index.ts                # MCP server bootstrap (stdio)
  tools/
    open-app.ts
    open-vscode-folder.ts
    git-push.ts
  resources/
    recent-projects.ts
  safety/allowlist.ts
```

## Done when

- [ ] Works end to end
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
