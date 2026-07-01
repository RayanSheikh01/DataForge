# DataForge

A synthetic training-data factory. DataForge generates high-quality
instruction-tuning pairs (prompt → response) using an **LLM-as-generator +
LLM-as-verifier** loop, filters near-duplicates, and writes a resumable JSONL
corpus that exports to a HuggingFace `datasets` (Arrow) dataset.

The LLM backend is a local [Ollama](https://ollama.com) server accessed through
its OpenAI-compatible REST API, so generation runs entirely offline on your own
models.

## How it works

```
YAML config
   │
   ▼
SeedSampler ──► Generator ──► Verifier ──┐
   ▲                             │       │ pass
   └──────── retry w/ critique ◄─┘ fail  ▼
                                       Deduper ──► Writer (JSONL) ──► HF dataset
```

For each target sample:

1. Sample a unique seed combination (e.g. topic × persona) for diversity.
2. Generate a candidate pair.
3. Verify it. The verifier returns `passed`, a 1–10 `score`, and a `critique`.
4. On failure, regenerate with the critique injected, up to `max_retries`.
5. On pass, drop near-duplicates; otherwise append the record and continue.

Runs are **resumable**: on restart, DataForge reads the existing JSONL, counts
accepted samples, skips already-used seed combinations, and continues to
`target_samples`.

## Install

Requires Python ≥ 3.11.

```
uv pip install -e ".[dev]"          # runtime + test deps
uv pip install -e ".[embedding]"    # optional: embedding-based dedup
```

To use the pipeline end-to-end you also need a running Ollama with the models
named in your config, e.g.:

```
ollama pull llama3.2:latest
```

## Usage

Configure a task in YAML (see [`examples/qa.yaml`](examples/qa.yaml)):

```yaml
task: customer-support-qa
model:
  generator: llama3.2:latest
  verifier: llama3.2:latest
  base_url: http://localhost:11434/v1
target_samples: 5
max_retries: 3
score_threshold: 7          # verifier 1-10
dedup:
  mode: lexical             # lexical | embedding | off
  threshold: 0.85
seeds:
  topic: [billing, returns, shipping, account]
  persona: [frustrated, polite, confused]
generator_template: templates/gen.j2
verifier_template: templates/verify.j2
output:
  dir: ./out/customer-support-qa
  push_to_hub: false
```

Then:

```
dataforge run examples/qa.yaml       # generate + verify + dedup into data.jsonl
dataforge export examples/qa.yaml    # build the HF dataset from data.jsonl
```

## Output layout

```
out/<task>/
  data.jsonl      # append-only, one record per line (source of truth, resumable)
  hf_dataset/     # Arrow dataset from `export`, load with datasets.load_from_disk
```

Each record carries `prompt`, `response`, the seed metadata, `verifier_score`,
and `attempts`.

## Prompt templates

Templates live in [`templates/`](templates/) and are rendered with Python's
`str.format()` (single-brace placeholders such as `{topic}`, `{critique}`),
despite the `.j2` extension. The generator emits a `PROMPT:` / `RESPONSE:` text
block; the verifier emits strict JSON `{"passed", "score", "critique"}`.

## Development

```
python -m pytest              # full offline suite (no Ollama required)
python -m pytest -m live      # live smoke tests against a real Ollama
```

Tests use an in-memory `FakeLLM` so the default suite never touches the network.
New work is written test-first.

## Docs

- [design.md](design.md) — architecture, decisions, data models, testing strategy.
- [implementation.md](implementation.md) — module-by-module build guide.
