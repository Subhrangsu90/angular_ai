# Tokens and the context window

Week 1 · How LLMs work · note 1

## Key ideas

### Tokens

- **A token is the unit an LLM reads and writes.** It is not a word or a character. It is a chunk of text from the model's fixed vocabulary, usually a word, part of a word, a space plus a word, or a symbol.
- **Text is split by a tokenizer**, usually a BPE (byte-pair encoding) variant. Common strings like `" the"` or `"function"` get one token each. Rare strings get split into several pieces (`"Angular"` → `"Ang"` + `"ular"` in some tokenizers).
- **Rule of thumb for English:** 1 token ≈ 4 characters ≈ ¾ of a word, so 100 tokens ≈ 75 words. It is only an estimate.
- **Some text costs more tokens than English prose:**
  - Code: braces, indentation and symbols often take a token each.
  - Non-English languages, especially non-Latin scripts such as Bengali or Hindi, can take 2–4× more tokens for the same meaning.
  - JSON: keys and quotes are repeated on every object.
  - Numbers and dates split in odd ways, which is part of why models are bad at arithmetic.
- **Each model family has its own tokenizer.** The same text gives different counts in GPT, Claude, Llama and Gemma. Measure with the tokenizer of the model you actually use.
- **Tokens drive everything you pay for or wait on:**
  - **Cost:** APIs charge per input token and per output token, and output is usually several times more expensive.
  - **Speed:** generation is measured in tokens per second, and output tokens are produced one at a time.
  - **Limits:** context size, max output and rate limits are all counted in tokens.

### Context window

- **The context window is the most tokens the model can handle in one request, counting both input and output.**
  - `input (system prompt + chat history + docs + tool definitions) + output ≤ context window`
- **The model is stateless.** It does not remember earlier messages. A chat app re-sends the whole conversation every turn, so each turn costs more than the last.
- **Max output tokens is a separate, smaller cap.** A model can have a very large window but only allow a few thousand tokens of output per response.
- **What happens when you go over depends on the tool:**
  - Hosted APIs usually return an error.
  - Some tools silently drop the oldest tokens. Ollama does this, and its default context is small.
  - Silent truncation is the dangerous case: the system prompt or the start of a document disappears and nothing warns you.
- **Window sizes vary a lot.** Small local models give a few thousand to ~128K tokens. Frontier APIs give hundreds of thousands to 1M+.
- **A bigger window has costs:**
  - **Cost and latency** grow with the number of input tokens.
  - **Recall gets worse.** Models pay most attention to the start and end of the context and miss facts buried in the middle ("lost in the middle").
  - **RAM/VRAM grows** with context length in local models (the KV cache), so raising `num_ctx` in Ollama can make a model stop fitting on your GPU.

### Managing the budget (what an app actually does)

1. **Count, don't guess.** Count tokens before sending and keep room for the reply: `budget = window − maxOutput − safety margin`.
2. **Trim chat history.** Keep the system prompt and the last N turns, and drop or summarize older turns.
3. **Retrieve, don't stuff.** Send only the relevant chunks, not whole documents. This is RAG, covered in note 04 (embeddings).
4. **Put important instructions at the start or end**, not in the middle.
5. **Cache stable prefixes.** Many APIs discount a repeated prefix such as a long system prompt or reference doc (prompt caching).
6. **Cap output** with `max_tokens` so cost and latency stay predictable.

## Tried it

**1. See token counts in Ollama.** `--verbose` prints the counts after each reply.

```bash
ollama run llama3.2 --verbose
>>> Explain Angular signals in one sentence.
# ...answer...
# prompt eval count:    34 token(s)     <- input tokens
# eval count:           41 token(s)     <- output tokens
# eval rate:            52.10 tokens/s  <- generation speed
```

**2. Check and raise a local model's context window.**

```bash
ollama show llama3.2              # "context length" = the most the model supports
ollama run llama3.2
>>> /set parameter num_ctx 8192   # what this session actually uses
```

Over the HTTP API, you pass the same setting as an option:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello",
  "stream": false,
  "options": { "num_ctx": 8192 }
}'
# the response JSON includes prompt_eval_count and eval_count
```

**3. Count tokens in TypeScript** (`npm i js-tiktoken`). This uses OpenAI's tokenizer, so for other model families treat the result as an estimate.

```ts
import { getEncoding } from 'js-tiktoken';

const enc = getEncoding('o200k_base');

const samples = {
  english: 'Signals make change detection in Angular more precise.',
  code: 'const count = signal(0); effect(() => console.log(count()));',
  bengali: 'সিগন্যাল অ্যাঙ্গুলারে পরিবর্তন শনাক্তকরণকে আরও নির্ভুল করে।',
};

for (const [label, text] of Object.entries(samples)) {
  console.log(label, text.length, 'chars →', enc.encode(text).length, 'tokens');
}
```

**4. Trim chat history to fit a budget**, the kind of logic that goes in an Angular chat service:

```ts
interface ChatMessage { role: 'system' | 'user' | 'assistant'; content: string }

const estimateTokens = (text: string) => Math.ceil(text.length / 4); // swap in a real tokenizer

export function fitToBudget(
  messages: ChatMessage[],
  contextWindow: number,
  maxOutput: number,
): ChatMessage[] {
  const [system, ...rest] = messages;
  let budget = contextWindow - maxOutput - estimateTokens(system.content) - 200; // safety margin
  const kept: ChatMessage[] = [];

  // Walk backwards so the most recent turns are kept first
  for (let i = rest.length - 1; i >= 0; i--) {
    const cost = estimateTokens(rest[i].content) + 4; // per-message overhead
    if (cost > budget) break;
    budget -= cost;
    kept.unshift(rest[i]);
  }
  return [system, ...kept];
}
```

## Gotchas / open questions

- **Silent truncation in Ollama.** If a long prompt "ignores" the system prompt, check `num_ctx` first. Raising it uses more RAM, so record that in the lab.
- **Chars/4 is wrong for code and non-English text.** Use a real tokenizer whenever cost or limits matter.
- **Hidden tokens count too:**
  - Chat templates and role markers add a few tokens per message.
  - Tool/function definitions and JSON schemas count as input.
  - Reasoning ("thinking") models spend output tokens on thinking you may never see.
- **Images and files are tokens too.** Multimodal input is converted to tokens and can be expensive.
- **Streaming changes nothing.** Streamed tokens cost the same; they just reach the user sooner.
- Open: how much does recall drop at 50% and 90% of a local model's window? Try a "needle in a haystack" test in the lab.
- Open: for a long-running chat in an Angular app, which works better: a summary of old turns, or retrieval over the full history?

## Links

- [OpenAI Tokenizer (interactive)](https://platform.openai.com/tokenizer): paste text and see how it splits into tokens
- [Tiktokenizer](https://tiktokenizer.vercel.app/): compares tokenizers across models
- [Andrej Karpathy: Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE): the best deep dive on BPE
- [Lost in the Middle (Liu et al., 2023)](https://arxiv.org/abs/2307.03172): why position in the context matters
- [Ollama FAQ: context window size](https://github.com/ollama/ollama/blob/main/docs/faq.md)
- [js-tiktoken on npm](https://www.npmjs.com/package/js-tiktoken)
- [Anthropic: token counting](https://docs.claude.com/en/docs/build-with-claude/token-counting) and [prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
