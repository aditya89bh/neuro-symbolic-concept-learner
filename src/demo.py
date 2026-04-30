from src.scene.scene_graph import SceneGraph
from src.reasoning.executor import SymbolicExecutor


def run_demo():
    scene = SceneGraph.from_json("examples/sample_scene.json")
    executor = SymbolicExecutor(scene)

    programs = [
        {
            "question": "What color is the cube?",
            "program": [
                {"op": "filter", "attribute": "shape", "value": "cube"},
                {"op": "query", "attribute": "color"},
            ],
        },
        {
            "question": "What is left of the blue sphere?",
            "program": [
                {"op": "filter", "attribute": "color", "value": "blue"},
                {"op": "filter", "attribute": "shape", "value": "sphere"},
                {"op": "relate", "relation": "left_of"},
                {"op": "query", "attribute": "color"},
            ],
        },
        {
            "question": "How many small objects are there?",
            "program": [
                {"op": "filter", "attribute": "size", "value": "small"},
                {"op": "count"},
            ],
        },
        {
            "question": "Is there a green cylinder?",
            "program": [
                {"op": "filter", "attribute": "color", "value": "green"},
                {"op": "filter", "attribute": "shape", "value": "cylinder"},
                {"op": "exist"},
            ],
        },
    ]

    for item in programs:
        print("\n==============================")
        print(f"Question: {item['question']}")

        result, trace = executor.execute(item["program"])

        print(f"Answer: {result}")
        print("Trace:")
        for step in trace:
            print(f" - {step}")


if __name__ == "__main__":
    run_demo()
