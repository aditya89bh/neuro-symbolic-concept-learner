from src.language.parser import QuestionParser


def test_parse_color_query():
    parser = QuestionParser()
    program = parser.parse("What color is the cube?")

    assert program == [
        {"op": "filter", "attribute": "shape", "value": "cube"},
        {"op": "query", "attribute": "color"},
    ]


def test_parse_size_query_with_multiple_filters():
    parser = QuestionParser()
    program = parser.parse("What size is the red cube?")

    assert program == [
        {"op": "filter", "attribute": "color", "value": "red"},
        {"op": "filter", "attribute": "shape", "value": "cube"},
        {"op": "query", "attribute": "size"},
    ]


def test_parse_left_relation_query():
    parser = QuestionParser()
    program = parser.parse("What is left of the blue sphere?")

    assert program == [
        {"op": "filter", "attribute": "color", "value": "blue"},
        {"op": "filter", "attribute": "shape", "value": "sphere"},
        {"op": "relate", "relation": "left_of"},
        {"op": "query", "attribute": "color"},
    ]


def test_parse_count_query():
    parser = QuestionParser()
    program = parser.parse("How many small objects are there?")

    assert program == [
        {"op": "filter", "attribute": "size", "value": "small"},
        {"op": "count"},
    ]


def test_parse_existence_query():
    parser = QuestionParser()
    program = parser.parse("Is there a green cylinder?")

    assert program == [
        {"op": "filter", "attribute": "color", "value": "green"},
        {"op": "filter", "attribute": "shape", "value": "cylinder"},
        {"op": "exist"},
    ]


def test_unsupported_question_returns_none():
    parser = QuestionParser()

    assert parser.parse("Why is the cube red?") is None
