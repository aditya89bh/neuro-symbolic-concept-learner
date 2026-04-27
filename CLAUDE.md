# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

The project has no external dependencies — everything uses Python stdlib only (`re`, `enum`, `dataclasses`, `math`, `typing`).

Run the full integration test suite (print-based, not pytest):
```bash
python test_complete_pipeline.py
python test_scene_graph.py
python test_logic_engine.py
python test_question_parser.py
```

Run the end-to-end demo:
```bash
python demo_working_pipeline.py
```

Run a single test function directly:
```bash
python -c "from test_complete_pipeline import test_basic_pipeline; test_basic_pipeline()"
```

## Architecture

The pipeline has three implemented modules and two stub modules (not yet implemented).

### Implemented modules

**`src/representation/scene_graph.py`** — The entry point for scene data. `SceneGraph` stores typed `Object` instances (with `Shape`, `Color`, `Material`, `Size` enums and a 3D `Position`) and `SpatialRelation` edges between them. The critical method is `to_predicates()`, which serialises the graph into flat predicate strings:
- `Object(obj_id, shape, color, material, size)` — note position is **dropped** in this conversion
- `Relation(obj1_id, relation_type, obj2_id)` — only relations where `value=True` are emitted

**`src/reasoning/logic_engine.py`** — `SimpleLogicEngine` ingests the predicate strings produced by `to_predicates()` and rebuilds them into two internal dicts: `self.objects` (id → property dict) and `self.relations` (list of 3-tuples). Queries are plain English strings dispatched by keyword matching in `query()`. The direct API (`find_objects_by_property`, `count_by_property`, `find_relations_between`, `compare_objects`) is more reliable than the `query()` string interface.

**`src/language/question_parser.py`** — `QuestionParser.parse()` takes a raw English question and returns a `StructuredQuery` dataclass with a `QueryType` enum and extracted fields. `StructuredQuery.to_logic_query()` converts it back to a string consumable by `SimpleLogicEngine.query()`. The parser uses ordered regex checks; the first matching pattern wins.

### Data flow

```
SceneGraph  ──to_predicates()──►  List[str]  ──►  SimpleLogicEngine
                                                          │
QuestionParser.parse(question)                    engine.query(str)
       │                                                  │
       ▼                                                  ▼
StructuredQuery ──to_logic_query()──► query_str     answer (Any)
```

### Stub modules (not yet implemented)

`src/vision/` and `src/concepts/` contain only docstring `__init__.py` files. The README describes intended components (CNN feature extraction, concept grounding, etc.) but no code exists there yet.

### Key invariants

- `SimpleLogicEngine.add_facts()` calls `_parse_facts()`, which **clears and rebuilds** `self.objects` and `self.relations` from scratch every time — so calling it repeatedly is safe but O(n) in total facts each time.
- `SceneGraph.to_predicates()` is lossy: 3D position data does not survive the round-trip through the predicate format.
- All valid CLEVR property values are fixed enums (`Shape`, `Color`, `Material`, `Size`, `SpatialRelation`). The logic engine stores values as lowercase strings after stripping; the question parser validates against hardcoded `valid_values` lists that must be kept in sync with these enums.
