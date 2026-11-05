# Agentic admin dashboard

Built in weeks 23–24. An admin dashboard for the e-commerce project where the model assembles real Angular components and an agent drafts product listings, with a visible step timeline and approval before saving.

## Planned structure

```
src/app/
  catalog/                 # components the model may use (whitelist)
    product-table.component.ts
    sales-chart.component.ts
    product-card.component.ts
    catalog.ts             # name → component + Zod prop schema
  renderer/
    ui-spec.schema.ts      # Zod schema for the JSON surface spec
    ui-renderer.component.ts   # ViewContainerRef.createComponent
  agent/
    agent-run.service.ts   # AG-UI event stream → signals
    step-timeline.component.ts
    tool-call-card.component.ts
    approval-dialog.component.ts
  pages/
    dashboard.page.ts
    listing-drafts.page.ts
server/
  agent.ts                 # AG-UI / CopilotKit runtime endpoint
  tools.ts                 # product API tools, role-checked
```

## Done when

- [ ] Works end to end
- [ ] Only whitelisted components render; every prop is validated
- [ ] README with setup, architecture, screenshot or demo video
- [ ] Pushed to GitHub (and deployed, if it has a UI)
