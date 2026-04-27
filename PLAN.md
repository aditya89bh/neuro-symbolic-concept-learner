# symbolic-memory-primitives

Sister repo to [`memory-and-intelligence-primitives`](https://github.com/). Code companion to the essay series.

---

## What this is

The executable companion to the `memory-and-intelligence-primitives` essays. Where those essays argue that structure matters for memory and retrieval, this repo demonstrates it. Two pipelines, same task, side by side: structured perception with structured retrieval vs. embedding-based retrieval. The contrast is the point.

The system also serves as a reference implementation of the IPCA model (Intent / Perception / Cognition / Action). Every module maps to one of those four layers.

## What it aims to achieve

1. Make the central thesis of the essay series concrete. Structured perception and structured retrieval do things that vector pipelines cannot. Show it, do not just argue it.
2. Provide the smallest readable IPCA loop that runs end to end.
3. Give essay readers something they can clone, run, and modify.
4. Build a corpus of failure-mode fixtures showing where vector retrieval breaks. Counting, negation, compositional queries, spatial relations, exclusion.
5. Stay small. This repo earns its keep by being readable, not impressive.

## IPCA mapping

| Layer | Module | Role |
|---|---|---|
| Intent | `src/language/` | Parses goal into structured query |
| Perception | `src/representation/` | Raw scene into structured representation |
| Cognition | `src/reasoning/` | Structured query over structured memory |
| Action | `src/action/` *(to be added)* | Returns and formats the answer |

## Status

**Phase 0 (current).** Legacy NSCL pipeline inherited from earlier work. Symbolic half implemented and tested. Neural half empty. README oversells what exists. `AGENTS.md` is more honest than README.

---

## Plan

### Phase 1: Reposition

Goal: stop shipping what we do not deliver. Be honest about what this is.

- [ ] Rename repo to `symbolic-memory-primitives`
- [ ] Delete `src/vision/` and `src/concepts/`
- [ ] Rewrite README around IPCA and the structured-vs-vector thesis
- [ ] Add Mermaid diagram of the IPCA mapping at the top of README
- [ ] Add `src/action/AnswerFormatter` so all four IPCA layers exist as modules
- [ ] Deduplicate `QueryType` enum (currently defined in two files)
- [ ] Fix `to_predicates()` so position survives the round-trip
- [x] Migrate print-based tests to pytest with real assertions
- [ ] Commit cleanly with a fresh framing

**Done when:** new reader lands on the README, understands what this is in under two minutes, and can run the demo.

### Phase 2: Contrast demo

Goal: show the thesis in execution, not just in argument.

- [ ] Add `baselines/vector_retrieval/`
- [ ] Build parallel pipeline: object embeddings, query embeddings, top-k retrieval, LLM answer
- [ ] Build `compare.py` that runs both pipelines over the same scenes and emits a side-by-side report
- [ ] Document failure categories: counting, negation, spatial relations, compositional, exclusion
- [ ] Save each failure case as a fixture so it becomes a regression test
- [ ] Write a results README summarizing the contrast

**Done when:** running `compare.py` produces a report that any reader of the essays would recognize as their thesis, in code.

### Phase 3: Essay integration

Goal: close the loop between argument and code.

- [ ] Add `WHY-THIS-REPO.md` tracing essay-to-code lineage
- [ ] Add "See the code" link to each relevant essay in `memory-and-intelligence-primitives`
  - [ ] Vector-DB essay → contrast demo and failure modes
  - [ ] State-vs-memory essay → scene graph as memory, engine working state as state
  - [ ] Cognitive-loops essay → full IPCA pipeline as minimum viable loop
- [ ] Cross-link from this repo's README back to each essay

**Done when:** any reader can move freely between essay and code without losing the thread.

---

## Out of scope

- Training neural components (CLEVR vision module, concept embeddings). The repo is symbolic by design, not by accident.
- Publication or research-artifact framing.
- Performance optimization. Readability beats throughput.

## How to use this document

A living plan. Check off items as they complete. Add notes inline as decisions get made. When all of Phase 3 is checked, the project is done. If a phase stops earning its keep, kill it. Sunk cost is sunk.
