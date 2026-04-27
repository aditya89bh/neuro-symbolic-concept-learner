"""Pytest tests for QuestionParser."""

import pytest
from src.language.question_parser import QuestionParser, QueryType


@pytest.fixture
def parser():
    return QuestionParser()


# --- Query type detection ---

@pytest.mark.parametrize("question", [
    "What color is the cube?",
    "What shape is the red object?",
    "What material is the blue sphere?",
    "What is the color of the red cube?",
    "What size is the metal cylinder?",
])
def test_property_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.PROPERTY


@pytest.mark.parametrize("question", [
    "How many red objects are there?",
    "Count the number of blue spheres",
    "How many objects are red?",
    "What is the total number of metal cubes?",
])
def test_count_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.COUNT


@pytest.mark.parametrize("question", [
    "What is left of the blue sphere?",
    "What object is right of the red cube?",
    "Find the object that is above the green cylinder",
    "What is behind the yellow sphere?",
])
def test_relation_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.RELATION


@pytest.mark.parametrize("question", [
    "Are there any metal cubes?",
    "Is there a red sphere?",
])
def test_existence_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.EXISTENCE


@pytest.mark.parametrize("question", [
    "Compare obj1 and obj2",
    "What is the difference between red_cube and blue_sphere?",
])
def test_comparison_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.COMPARISON


@pytest.mark.parametrize("question", [
    "What is the meaning of life?",
    "How do I cook pasta?",
    "What time is it?",
    "Random text that doesn't make sense",
])
def test_unknown_query_type(parser, question):
    assert parser.parse(question).query_type == QueryType.UNKNOWN


# --- Field extraction ---

def test_property_query_fields(parser):
    result = parser.parse("What color is the cube?")
    assert result.target_property == "color"
    assert result.target_object == "cube"


def test_count_query_fields(parser):
    result = parser.parse("How many red objects are there?")
    assert result.target_value == "red"


def test_comparison_objects_extracted(parser):
    result = parser.parse("Compare obj1 and obj2")
    assert result.comparison_objects == ["obj1", "obj2"]


def test_existence_conditions_extracted(parser):
    result = parser.parse("Are there any metal cubes?")
    assert result.conditions is not None
    assert len(result.conditions) > 0


# --- Validation ---

@pytest.mark.parametrize("question", [
    "What color is the cube?",
    "How many red objects are there?",
    "What is left of the blue sphere?",
    "Are there any metal cubes?",
])
def test_validate_question_valid(parser, question):
    assert parser.validate_question(question) is True


@pytest.mark.parametrize("question", [
    "What is the meaning of life?",
    "How do I cook pasta?",
    "Random text",
])
def test_validate_question_invalid(parser, question):
    assert parser.validate_question(question) is False


# --- to_logic_query ---

def test_to_logic_query_non_empty_for_known_types(parser):
    for question in [
        "What color is the cube?",
        "How many red objects are there?",
        "Are there any metal cubes?",
        "Compare obj1 and obj2",
    ]:
        result = parser.parse(question)
        assert result.to_logic_query() != ""


def test_to_logic_query_unknown_falls_back_to_raw(parser):
    q = "What is the meaning of life?"
    result = parser.parse(q)
    assert result.to_logic_query() == q.lower().strip()
