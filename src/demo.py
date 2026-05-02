from src.scene.scene_graph import SceneGraph
from src.reasoning.executor import SymbolicExecutor
from src.language.parser import QuestionParser


def run_demo():
    scene = SceneGraph.from_json("examples/sample_scene.json")
    executor = SymbolicExecutor(scene)
    parser = QuestionParser()

    questions = [
        "What color is the cube?",
        "What is left of the blue sphere?",
        "How many small objects are there?",
        "Is there a green cylinder?",
    ]

    for question in questions:
        print("\n==============================")
        print(f"Question: {question}")

        program = parser.parse(question)

        if not program:
            print("Could not parse question")
            continue

        print(f"Program: {program}")

        result, trace = executor.execute(program)

        print(f"Answer: {result}")
        print("Trace:")
        for step in trace:
            print(f" - {step}")


if __name__ == "__main__":
    run_demo()
