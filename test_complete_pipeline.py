"""End-to-end pytest tests for the full NSCL pipeline."""

import pytest
from src.representation.scene_graph import (
    SceneGraph, Shape, Color, Material, Size, SpatialRelation, Position
)
from src.reasoning.logic_engine import SimpleLogicEngine
from src.language.question_parser import QuestionParser, QueryType


@pytest.fixture
def scene():
    g = SceneGraph()
    obj1 = g.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    obj2 = g.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(2, 0, 0))
    obj3 = g.add_object(Shape.CYLINDER, Color.GREEN, Material.METAL, Size.LARGE, Position(1, 1, 0))
    g.add_relation(obj1, SpatialRelation.LEFT_OF, obj2)
    g.add_relation(obj3, SpatialRelation.ABOVE, obj1)
    return g, obj1, obj2, obj3


@pytest.fixture
def engine(scene):
    g, *_ = scene
    return SimpleLogicEngine(g.to_predicates())


@pytest.fixture
def parser():
    return QuestionParser()


# --- Scene → predicate → engine round-trip ---

def test_predicates_loaded(scene, engine):
    g, *_ = scene
    assert len(engine) == len(g)


def test_relations_loaded(scene, engine):
    g, *_ = scene
    true_rels = sum(1 for v in g.relations.values() if v)
    assert len(engine.get_all_relations()) == true_rels


def test_count_metal_objects(engine):
    assert engine.count_by_property("material", "metal") == 2


def test_count_large_objects(engine):
    assert engine.count_by_property("size", "large") == 2


def test_find_red_object(scene, engine):
    _, obj1, *_ = scene
    assert engine.find_objects_by_property("color", "red") == [obj1]


def test_find_blue_object(scene, engine):
    _, _, obj2, _ = scene
    assert engine.find_objects_by_property("color", "blue") == [obj2]


def test_spatial_relation_preserved(scene, engine):
    _, obj1, obj2, _ = scene
    rels = engine.find_relations_between(obj1, obj2)
    assert len(rels) == 1
    assert rels[0][1] == "left_of"


def test_compare_objects(scene, engine):
    _, obj1, obj2, _ = scene
    result = engine.compare_objects(obj1, obj2)
    assert "similarities" in result
    assert "differences" in result


# --- Question parser integration ---

def test_property_question_pipeline(engine, parser):
    result = parser.parse("What color is the cube?")
    assert result.query_type == QueryType.PROPERTY
    logic_q = result.to_logic_query()
    assert logic_q != ""


def test_count_question_pipeline(engine, parser):
    result = parser.parse("How many red objects are there?")
    assert result.query_type == QueryType.COUNT
    logic_q = result.to_logic_query()
    answer = engine.query(logic_q)
    assert isinstance(answer, int)


def test_existence_question_pipeline(engine, parser):
    result = parser.parse("Are there any metal cubes?")
    assert result.query_type == QueryType.EXISTENCE
    logic_q = result.to_logic_query()
    assert logic_q != ""


def test_unsupported_questions_do_not_crash(engine, parser):
    for q in ["What is the meaning of life?", "How do I cook pasta?", "Random text"]:
        result = parser.parse(q)
        assert result.query_type == QueryType.UNKNOWN
