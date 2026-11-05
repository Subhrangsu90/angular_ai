# AI Path for an Angular Developer: 24-Week Plan

Nov 4, 2026 · @Subhrangsu

## How to use this plan

The plan takes 24 weeks at about 8–10 hours a week, alongside a full-time job. Every phase ends with a shipped project on GitHub, not just notes.

| Day | Time | What |
| --- | --- | --- |
| Mon–Thu | 1 hr each | Learn: docs, a course module, or a short tutorial |
| Sat | 3 hrs | Build: the week's hands-on task |
| Sun | 1–2 hrs | Ship: push code, write a short README or LinkedIn post |

Rules:

- Build in Angular wherever possible. Your edge is AI plus great frontend, not Python ML.
- Use one hosted model (Claude, Gemini or OpenAI free tier) and one or more local models via Ollama side by side, picked per task (see the next section).
- Your i5 with 16 GB RAM handles small local models (2B–4B). Use hosted APIs for anything heavier.
- Falling behind is fine. Push a week back rather than skipping the build task.

## Choosing a local model

Pick the open model that fits each task, not one model for everything. Every code path in this plan stays model-agnostic: the model name is a config value.

| Requirement | Model families to try | Size that runs on 16 GB RAM, no GPU |
| --- | --- | --- |
| General chat, writing | Llama, Gemma, Qwen, Mistral | 3B–8B, 4-bit quantized |
| Code help, agents, tool calling | Qwen Coder, DeepSeek Coder, Llama | 7B–8B, 4-bit |
| Fast or low-RAM (phone, browser) | Gemma small, Phi, Qwen small, SmolLM | 0.5B–3B |
| Embeddings for RAG | nomic-embed-text, bge, all-MiniLM | Under 0.5B |
| Speech to text | Whisper (tiny, base, small) | Under 0.5B |
| Images in, text out | LLaVA, Llama Vision, Gemma vision variants | 4B–8B, slow on CPU |

How to choose:

- Check the Ollama model library and Hugging Face for the newest version of each family; they change every few months.
- Test 2–3 candidates on 10 of your own prompts. Compare quality, speed (tokens per second) and RAM.
- Check the licence before using a model in a client project.
- Use a hosted model when no local model is good enough.

## Phase 1 (Weeks 1–3): AI fundamentals

Goal: understand how LLMs behave and call them from code. Deliverable: a Node CLI that talks to a hosted model and any local model.

**Week 1: How LLMs work**

- [ ] Learn tokens, context window, temperature, top-p, system vs user messages
- [ ] Learn embeddings at a concept level: text turned into vectors, similarity search
- [ ] Learn why models hallucinate and how grounding reduces it
- [ ] Build: install Ollama, pull 2–3 models (e.g. Llama, Qwen, Gemma), chat with it from the terminal

**Week 2: Prompt engineering**

- [ ] Practice system prompts, few-shot examples, role prompts
- [ ] Get structured JSON output reliably, and validate it with Zod
- [ ] Compare the same prompt across your local models and a hosted model; note quality and speed
- [ ] Build: a prompt playground script that saves prompts and outputs to a file

**Week 3: Calling APIs from code**

- [ ] Get an API key for one hosted provider; call it from Node with its SDK
- [ ] Learn streaming responses (server-sent events) in Node
- [ ] Learn rate limits, token counting and cost per request
- [ ] Build: `ai-cli` — one command, switch provider and model with a flag. Push to GitHub.

## Phase 2 (Weeks 4–7): AI inside Angular apps

Goal: build production-quality AI UIs with signals. Deliverable: a streaming chat app with a model switcher, deployed online.

**Week 4: Backend proxy**

- [ ] Build a small Express server that holds API keys and forwards requests
- [ ] Stream model output to the browser over SSE
- [ ] Add a simple per-IP rate limit
- [ ] Build: `/api/chat` endpoint that streams from any local or hosted model

**Week 5: Streaming chat UI**

- [ ] Consume the stream with `fetch` + `ReadableStream`; append tokens into a signal
- [ ] Render markdown and code blocks with syntax highlighting
- [ ] Add stop/cancel with `AbortController`, retry, and error states
- [ ] Build: chat component with message list, input, stop button

**Week 6: Real-app features**

- [ ] Save conversation history (localStorage first, then Postgres)
- [ ] Add a system-prompt editor and model dropdown
- [ ] Learn Genkit or Firebase AI Logic and try one flow with it
- [ ] Build: add these features to the chat app

**Week 7: AI inside your editor**

- [ ] Add slash commands to your ProseMirror editor: /rewrite, /summarize, /fix grammar
- [ ] Stream the AI result into the document as a suggestion the user accepts or rejects
- [ ] Ship: deploy the chat app; write a post on streaming AI in Angular with signals

## Phase 3 (Weeks 8–11): RAG and tool calling

Goal: make AI answer from your own data and act through your APIs. Deliverable: a "chat with your docs" app and AI product search.

**Week 8: Embeddings and vector search**

- [ ] Generate embeddings with a hosted API or a local embedding model in Ollama
- [ ] Install pgvector in Postgres; store and query vectors
- [ ] Learn cosine similarity and top-k retrieval
- [ ] Build: semantic search over 50 text snippets

**Week 9: RAG pipeline**

- [ ] Chunk documents (size, overlap), embed, store
- [ ] Retrieve, add chunks to the prompt, answer with source citations
- [ ] Build: Angular "chat with your docs" — upload PDF or markdown, ask questions, show sources

**Week 10: Function calling / tool use**

- [ ] Learn how a model picks a tool and returns arguments as JSON
- [ ] Write 2–3 tools: search products, get order status, get weather
- [ ] Show tool calls in the UI as cards ("Searching products…")
- [ ] Build: AI shopping assistant that calls your product API

**Week 11: Apply to the e-commerce project**

- [ ] Natural-language product search ("comfortable everyday wear under ₹1,500") with pgvector
- [ ] Generate product descriptions in the admin panel
- [ ] Ship: demo video plus README covering the RAG architecture

## Phase 4 (Weeks 12–15): AI in the browser and voice

Goal: run models on the user's device, where few frontend devs are skilled. Deliverable: the spoken-English practice app.

**Week 12: On-device models**

- [ ] Try Transformers.js: sentiment, summarization, embeddings in the browser
- [ ] Run a small LLM in the browser with WebLLM (Llama, Qwen, Phi, Gemma) or MediaPipe LLM Inference
- [ ] Use a Web Worker so the UI never freezes; show model-download progress
- [ ] Build: offline AI text tool in Angular

**Week 13: Speech in and out**

- [ ] Speech-to-text: Web Speech API, then Whisper (in-browser or local)
- [ ] Text-to-speech: browser speechSynthesis
- [ ] Handle microphone permissions and recording UI states
- [ ] Build: voice chat — speak, AI replies aloud

**Week 14: Spoken-English app (core)**

- [ ] Topic prompts for work situations: standup, code review, interview
- [ ] Transcribe the answer; the chosen model returns grammar fixes, better phrasing, a 1–10 score as JSON
- [ ] Build: practice screen plus feedback screen

**Week 15: Spoken-English app (polish)**

- [ ] Save sessions and show progress over time
- [ ] Add speaking-speed (words per minute) and filler-word count
- [ ] Ship: deploy as a PWA; record a demo

## Phase 5 (Weeks 16–20): Agents, MCP, production, npm library

Goal: build multi-step agents and ship reusable work. Deliverables: an MCP server, a local voice controller, and an `ngx-ai` npm package.

**Week 16: Agents**

- [ ] Learn the agent loop: plan → call tool → observe → repeat, with a step limit
- [ ] Add human approval before risky actions
- [ ] Build: an agent that reads a GitHub issue and drafts a fix plan

**Week 17: MCP (Model Context Protocol)**

- [ ] Learn MCP servers, tools and resources
- [ ] Write an MCP server in TypeScript exposing your own tools
- [ ] Build: MCP server for your laptop — open app, open VS Code folder, git push

**Week 18: Voice laptop controller**

- [ ] Combine Whisper + a tool-calling local model (Qwen or Llama work well) + your MCP tools into a voice command loop
- [ ] Map intents to safe, allow-listed commands only
- [ ] Build: say "open the inkframe folder in VS Code" and it works

**Week 19: Production skills**

- [ ] Evals: a test set of 20 prompts with expected outputs; run it on every prompt change
- [ ] Cost and latency logging; response caching
- [ ] AI UX: show sources, allow undo, mark AI content, handle low confidence
- [ ] Read about prompt injection and guard your tools against it

**Week 20: Publish the npm library**

- [ ] Extract your best components: streaming chat, message list, markdown renderer, stream service
- [ ] Signal-based APIs, provider-agnostic adapters (hosted, Ollama, in-browser)
- [ ] Ship: publish `ngx-ai-chat` (or similar) with docs and a demo site

After week 24, consider LoRA fine-tuning of the best-fitting open model for Inkframe, only if prompting plus RAG fall short.

## Phase 6 (Weeks 21–24): Generative and agentic UI

Goal: let the model choose and assemble your real Angular components, and build UIs that show an agent's steps, shared state and approvals. Deliverable: an agentic admin dashboard for the e-commerce project.

**Week 21: Generative UI from scratch**

- [ ] Learn the spectrum: text → tool-call cards → model picks from a component catalog → model describes a whole surface in JSON
- [ ] Learn why catalog-based is the safe default: the model only uses components you expose, never raw HTML or code
- [ ] Build your own renderer: model returns a JSON spec, validate it with Zod, map it to components with `ViewContainerRef.createComponent`, render partial JSON while it streams
- [ ] Build: "show my top products this month" answers with a table or chart component, not text

**Week 22: Hashbrown (Angular-native generative UI)**

- [ ] Expose components with `exposeComponent`, typed with Skillet schemas; use the signal-based `uiChatResource`
- [ ] Try its recipes: natural-language forms, predictive suggestions, chatbot with tools
- [ ] Wrap design-system components in smart wrappers that handle DI, stores and router
- [ ] Build: generative UI chat over your own component library

**Week 23: Agentic UI with AG-UI and CopilotKit**

- [ ] Learn AG-UI events: run start/finish, text deltas, tool calls, state snapshots and deltas
- [ ] Use CopilotKit for Angular: prebuilt chat or headless mode, shared state, human-in-the-loop
- [ ] Learn agent UX patterns: step timeline, live tool-call cards, editable plan, approve or reject before an action, interrupt and resume
- [ ] Build: an agent that drafts product listings; the user watches each step and approves before saving

**Week 24: A2UI, MCP Apps and safety**

- [ ] A2UI: agent-described surfaces rendered with `@a2ui/angular`; add a custom catalog of your components
- [ ] MCP Apps: tool results shown as interactive widgets inside the chat
- [ ] Safety: whitelist components, validate every prop, expose components by user role, never execute model-written code outside a sandbox
- [ ] Ship: agentic admin dashboard demo; add a generative-UI renderer to your npm library; write "Generative UI in Angular" post

## Portfolio checklist and milestones

By week 24 you should have seven shipped projects and one npm package. Dates assume a start on Monday 9 Nov 2026.

| Week | Target date | Milestone | Proof |
| --- | --- | --- | --- |
| 3 | 29 Nov 2026 | `ai-cli` hosted + local models | GitHub repo |
| 7 | 27 Dec 2026 | Streaming Angular chat app + editor AI commands | Live URL, blog post |
| 11 | 24 Jan 2027 | Chat-with-docs + AI product search | Demo video |
| 15 | 21 Feb 2027 | Spoken-English practice PWA | Live PWA |
| 18 | 14 Mar 2027 | MCP server + voice laptop controller | Demo video |
| 20 | 28 Mar 2027 | `ngx-ai-chat` on npm | npm page, docs site |
| 24 | 25 Apr 2027 | Generative + agentic UI admin dashboard | Demo video, blog post |

After each milestone:

- [ ] Update your resume line: "Built X with Angular + LLMs, which does Y"
- [ ] Post a short write-up on LinkedIn or dev.to
- [ ] Pin the repo on your GitHub profile

## Resources

Mostly free official docs; search each name to find the current page.

| Phase | Resource | Use it for |
| --- | --- | --- |
| 1 | Anthropic prompt engineering guide (docs.claude.com) | Prompting fundamentals |
| 1 | Ollama docs | Running any open model locally |
| 1 | Andrej Karpathy, "Intro to Large Language Models" (YouTube) | How LLMs work |
| 2 | angular.dev AI section; Genkit docs | Angular + AI patterns |
| 2 | Vercel AI SDK docs | Streaming and chat UI patterns to borrow |
| 3 | pgvector README | Vector search in Postgres |
| 3 | DeepLearning.AI short courses (RAG, function calling) | Free 1–2 hour courses |
| 4 | Transformers.js docs (Hugging Face) | In-browser models |
| 4 | MediaPipe LLM Inference (Google AI Edge); WebLLM | LLMs in the browser |
| 5 | modelcontextprotocol.io and the TypeScript SDK | Building MCP servers |
| 5 | Hugging Face "LLM Course" / Unsloth docs | Fine-tuning open models later |

Phase 6 links:

- [Hashbrown docs, Angular quick start](https://hashbrown.dev/docs/angular/start/quick) — open-source generative UI for Angular, signal-based
- [CopilotKit Angular announcement](https://dev.to/copilotkit/introducing-angular-support-for-copilotkit-bring-any-agent-into-your-app-2f3e) — AG-UI agents in Angular with generative UI, shared state, human-in-the-loop
- [A2UI spec](https://a2ui.org/) — Google's agent-to-UI protocol with an Angular renderer
- [Angular Architects: A2UI in Angular](https://www.angulararchitects.io/en/blog/a2ui-how-ai-generates-dynamic-uis-at-runtime/) — blog series covering AG-UI, A2UI, custom catalogs and MCP Apps in Angular
- [Generative UI in Angular with a JSON spec](https://dev.to/shteynu/generative-ui-in-angular-the-llm-streams-a-json-spec-you-render-real-components-4lgf) — build-your-own renderer approach for week 21
