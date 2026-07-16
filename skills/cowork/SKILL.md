---
name: cowork
description: When the user says "коворк" / "cowork" / "кворк" followed by a task, generate a single self-contained prompt the user will copy-paste into a browser-based agent (Comet, ChatGPT Atlas, Claude.ai, Perplexity, Gemini, Manus). Output is ALWAYS one paste-ready prompt block, no preamble, no trailing questions. Browser agent does the actual work; this skill only produces the prompt.
---

# cowork — Browser-Ready Prompt Generator

## What this is

The user has subscriptions to multiple browser-based AI agents (ChatGPT Team, ChatGPT Plus, Claude Max, Perplexity Pro, sometimes Comet/Atlas). They want to offload heavy research / web-action tasks to those agents instead of burning Claude Code context/budget. You are the "prompt factory" — when they say *cowork*, you produce one fully self-contained prompt they paste into a browser tab.

The user is already logged into all of those tools. The browser agent has its own web/tool access. You don't.

## Trigger phrases

User says any of: `коворк`, `cowork`, `кворк`, `co-work`, `браузерний агент`, `зроби промпт для cowork`, `дай coworkprompt`, followed by a task description.

## Output protocol — RIGID

When triggered, your entire response is:

1. **One single sentence** above the block describing what the prompt does and where to paste (e.g., "Промпт для повного keyword research у Comet/ChatGPT — копіюй усе нижче, вставляй у новий чат.")
2. **One triple-backtick code block** containing the prompt itself (so user copies with one click).
3. **Nothing after the block.** No "let me know if…", no follow-ups, no clarifications. The user iterates if they need to.

If the task is **truly ambiguous** (e.g., the user said only "коворк зроби щось" with no object), ask exactly ONE clarifying question. Otherwise produce confidently.

## What goes inside the prompt

A good cowork prompt is 400–1500 words and contains, in order:

1. **Role / persona** — who the browser agent is acting as. Be specific ("senior B2B SEO strategist", not "helpful assistant").
2. **Mission** — one sentence, concrete deliverable.
3. **Context the agent needs** — URLs, file references, what the user is building, why this matters. Bake in everything; assume the agent has zero prior context.
4. **Inputs available in browser** — "You can browse the web. You can read URLs the user is logged into (ChatGPT/Gmail/etc.). You can use code interpreter / data analysis if available."
5. **Process** — numbered steps the agent should follow. Be opinionated about method (e.g., "scrape Reddit threads, not just summarise from memory").
6. **Output format** — exactly what to deliver: markdown file? table? canvas doc? Download as .md? Paste back into chat?
7. **Constraints** — what NOT to do (don't fabricate stats, cite sources inline, no fluff intro), when to ask the user (almost never — make decisions and proceed).
8. **Success criteria** — measurable (e.g., "≥200 keywords", "10 competitors profiled with URLs", "5 quick wins flagged").

## Defaults to bake in

Unless the user says otherwise:

- **Language:** prompt in English (most browser agents perform better in EN), but instruct the agent that the user's final content language is **Ukrainian for prose, English for technical terms** — agent should flag UA-specific vs global-EN keywords/insights.
- **Persona of the user:** senior software engineer / founder, anti-cloud bias, self-hosts, comfortable with intermediate-advanced material — skip 101-level explanations.
- **Output:** markdown, copy-paste-ready, with `[source](url)` citations inline. No emoji unless user asked.
- **Decisiveness:** agent makes calls and ships; doesn't ask the user follow-ups mid-task.
- **Length:** "comprehensive over concise" — these are async deep-research tasks; the user wants depth, not a summary.

## Anti-patterns

- ❌ Asking the user to "fill in" placeholders — the prompt must work as-is on paste.
- ❌ Generic instructions like "research X thoroughly" — be opinionated about *what* to look at and *how*.
- ❌ Wrapping the prompt in your own commentary that the user has to strip out before pasting.
- ❌ Multiple code blocks split across explanation — one block, one paste.
- ❌ Recommending the user run web searches themselves — the whole point is the browser agent does it.

## When the task references a file in the repo

If the user says "коворк виконай те що в `research/foo.md`" — open the file, summarize the brief into the prompt body (don't tell the agent "read this file" — agent can't), and instruct delivery.

## Worked examples

### Example 1 — Research

User: `коворк зроби competitive analysis для self-hosted PaaS landscape`

You output one sentence + one code block. The block has: persona = "senior B2B competitive intelligence analyst doing landscape research for an indie self-hosted PaaS"; mission = "produce a 15-competitor matrix"; context = brief on what self-hosted PaaS means + that the user runs Coolify on his Proxmox homelab; process = 7 steps with specific sources (GitHub stars, Reddit r/selfhosted threads, HN comments, individual project docs); output = markdown table + 1-paragraph profile per competitor + 5 strategic insights at end; constraints = no marketing fluff, cite every claim; success = exactly 15 competitors covering open-source + commercial + DIY tiers.

### Example 2 — Web action

User: `коворк знайди 10 топ homelab YouTube каналів і збери їхні метрики`

You output one sentence + one code block. The block has: persona = "YouTube growth analyst"; mission = "10-channel ranked table"; process = "Search YouTube + Social Blade + NoxInfluencer, dedupe, rank by composite score of subs + recent 30-day views + engagement"; output = markdown table with columns (channel, URL, subs, avg views/30d, upload cadence, dominant topics, monetisation signal); constraints = exclude channels last uploaded >90 days ago.

### Example 3 — File-driven

User: `коворк виконай research/home-office-homelab-keywords-prompt.md`

You read that file, then output one sentence + one code block that embeds the brief's deliverables/constraints as inline instructions for the browser agent (since the agent cannot open local files). End with "Deliver the result as one markdown file downloadable from chat, plus the same content pasted into the conversation."

## Why a skill and not an agent

Cowork is not a running process — there's no daemon, no MCP server, no SSH target. It is purely a **template + style guide** for one-off prompt generation. Lives as a skill so it auto-triggers on the user's phrasing in any project.
