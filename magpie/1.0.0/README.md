# magpie

An agent that mines another team's open source repository or package for engineering approaches worth adopting. It answers "what is done **well** here, **how** is it done, and is it worth taking" rather than "what does this repo contain".

## What it does

Three stages in one agent context:

1. **Extract** with the Vercel `opensrc` CLI — shallow clones the exact released version of an npm, PyPI, or crates package, or a GitHub repo.
2. **Map** with `graphify` — builds a directed knowledge graph of the code (deterministic AST path, no token cost), surfacing god nodes, communities, and surprising connections.
3. **Research** the map — reads the real source behind the structurally important code, traces mechanisms, scores each candidate against a fixed merit lens, then filters out anything lacking a concrete tradeoff it wins.

## Outputs

- **Pattern Catalogue** report (markdown) — one entry per kept pattern, rejected candidates noted with reasons.
- **Snippets folder** — the actual excerpts with attribution (source URL, file:line, licence).
- **Retained graph** — `graphify-out/` kept so the repo can be re queried with `/graphify query`.

A run lands a `magpieRuns/<target>/` folder in the invoking directory.

## Requirements

This plugin shells out to two external binaries that must be installed and on PATH:

- **opensrc** — Vercel's source fetching CLI. Install via the prebuilt binary from `github.com/vercel-labs/opensrc/releases`, `npm install -g opensrc` (Node 18+), or `brew install opensrc`.
- **graphify** — `pip install graphifyy`.

If either is missing the agent will stop at the relevant stage and report it.

## Usage

```
> Use the magpie agent to mine vercel/next.js/packages/next/src/server for streaming patterns
> Use the magpie agent: what can we learn from fastapi about dependency injection?
```
