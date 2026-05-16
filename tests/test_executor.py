from src.scene.scene_graph import SceneGraph
from src.reasoning.executor import SymbolicExecutor


SCENE_PATH = "examples/sample_scene.json"


def get_executor():
    scene = SceneGraph.from_json(SCENE_PATH)
    return SymbolicExecutor(scene)


def test_color_query_execution():
    executor = get_executor()

    program = [
        {"op": "filter", "attribute": "shape", "value": "cube"},
        {"op": "query", "attribute": "color"},
    ]

    result, trace = executor.execute(program)

    assert result == "red"
    assert len(trace) > 0


def test_relation_query_execution():
    executor = get_executor()

    program = [
        {"op": "filter", "attribute": "color", "value": "blue"},
        {"op": "filter", "attribute": "shape", "value": "sphere"},
        {"op": "relate", "relation": "left_of"},
        {"op": "query", "attribute": "color"},
    ]

    result, trace = executor.execute(program)

    assert result == "red"
    assert any("left_of" in step for step in trace)


def test_count_query_execution():
    executor = get_executor()

    program = [
        {"op": "filter", "attribute": "size", "value": "small"},
        {"op": "count"},
    ]

    result, _ = executor.execute(program)

    assert result == 2


def test_exist_query_execution():
    executor = get_executor()

    program = [
        {"op": "filter", "attribute": "color", "value": "green"},
        {"op": "filter", "attribute": "shape", "value": "cylinder"},
        {"op": "exist"},
    ]

    result, _ = executor.execute(program)

    assert result is True
