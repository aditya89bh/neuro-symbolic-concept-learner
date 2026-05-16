from src.language.parser import QuestionParser
from src.reasoning.executor import SymbolicExecutor
from src.scene.scene_graph import SceneGraph


EVALUATION_SET = [
    {
        "question": "What color is the cube?",
        "expected": "red",
    },
    {
        "question": "What size is the red cube?",
        "expected": "small",
    },
    {
        "question": "What is left of the blue sphere?",
        "expected": "red",
    },
    {
        "question": "What is right of the red cube?",
        "expected": "blue",
    },
    {
        "question": "How many small objects are there?",
        "expected": 2,
    },
    {
        "question": "Is there a green cylinder?",
        "expected": True,
    },
]


def evaluate():
    scene = SceneGraph.from_json("examples/sample_scene.json")
    parser = QuestionParser()
    executor = SymbolicExecutor(scene)

    total = len(EVALUATION_SET)
    correct = 0
    failed_parses = 0
    traces_present = 0

    print("Neuro-Symbolic Concept Learner Evaluation")
    print("========================================")

    for index, item in enumerate(EVALUATION_SET, start=1):
        question = item["question"]
        expected = item["expected"]

        program = parser.parse(question)
        if not program:
            failed_parses += 1
            print(f"{index}. FAIL_PARSE | {question}")
            continue

        result, trace = executor.execute(program)
        is_correct = result == expected

        if is_correct:
            correct += 1

        if trace:
            traces_present += 1

        status = "PASS" if is_correct else "FAIL"
        print(f"{index}. {status} | {question}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {result}")
        print(f"   Trace:    {'present' if trace else 'missing'}")

    accuracy = correct / total if total else 0
    trace_coverage = traces_present / total if total else 0

    print("\nSummary")
    print("-------")
    print(f"Total questions: {total}")
    print(f"Correct answers: {correct}")
    print(f"Accuracy: {accuracy:.0%}")
    print(f"Failed parses: {failed_parses}")
    print(f"Trace coverage: {trace_coverage:.0%}")


if __name__ == "__main__":
    evaluate()
