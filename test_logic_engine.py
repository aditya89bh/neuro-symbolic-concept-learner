"""Pytest tests for SimpleLogicEngine."""

import pytest
from src.reasoning.logic_engine import SimpleLogicEngine


BASIC_FACTS = [
    "Object(obj1, cube, red, metal, large)",
    "Object(obj2, sphere, blue, rubber, small)",
    "Object(obj3, cylinder, green, metal, large)",
    "Object(obj4, cube, yellow, rubber, small)",
    "Relation(obj1, left_of, obj2)",
    "Relation(obj3, above, obj1)",
    "Relation(obj4, right_of, obj2)",
]


@pytest.fixture
def engine():
    return SimpleLogicEngine(BASIC_FACTS)


def test_object_count(engine):
    assert len(engine) == 4


def test_get_all_objects(engine):
    assert set(engine.get_all_objects()) == {"obj1", "obj2", "obj3", "obj4"}


def test_get_object_properties(engine):
    props = engine.get_object_properties("obj1")
    assert props == {"shape": "cube", "color": "red", "material": "metal", "size": "large"}


def test_get_object_properties_missing(engine):
    assert engine.get_object_properties("nonexistent") is None


def test_find_by_property(engine):
    assert set(engine.find_objects_by_property("shape", "cube")) == {"obj1", "obj4"}
    assert engine.find_objects_by_property("color", "red") == ["obj1"]
    assert set(engine.find_objects_by_property("material", "metal")) == {"obj1", "obj3"}


def test_find_by_unknown_property(engine):
    assert engine.find_objects_by_property("unknown", "value") == []


def test_count_by_property(engine):
    assert engine.count_by_property("shape", "cube") == 2
    assert engine.count_by_property("color", "red") == 1
    assert engine.count_by_property("material", "metal") == 2
    assert engine.count_by_property("size", "large") == 2
    assert engine.count_by_property("color", "purple") == 0


def test_query_find_with_where(engine):
    assert set(engine.query("find objects where shape is cube")) == {"obj1", "obj4"}
    assert engine.query("find objects where color is red") == ["obj1"]


def test_query_count_with_where(engine):
    assert engine.query("count objects where shape is cube") == 2
    assert engine.query("count objects where color is red") == 1


def test_find_relations_between(engine):
    rels = engine.find_relations_between("obj1", "obj2")
    assert len(rels) == 1
    assert rels[0] == ("obj1", "left_of", "obj2")


def test_find_relations_between_unknown(engine):
    assert engine.find_relations_between("obj1", "obj4") == []


def test_query_relations_between(engine):
    result = engine.query("find relations between obj1 and obj2")
    assert len(result) == 1


def test_compare_objects_same_shape():
    eng = SimpleLogicEngine([
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, cube, red, metal, small)",
    ])
    result = eng.compare_objects("obj1", "obj2")
    assert "similarities" in result
    assert "differences" in result
    assert any("shape" in s for s in result["similarities"])
    assert any("size" in d for d in result["differences"])


def test_compare_objects_missing():
    eng = SimpleLogicEngine(["Object(obj1, cube, red, metal, large)"])
    assert eng.compare_objects("obj1", "nonexistent") == {}


def test_query_compare(engine):
    result = engine.query("compare obj1 and obj2")
    assert isinstance(result, dict)
    assert "similarities" in result


def test_add_facts_incremental():
    eng = SimpleLogicEngine(["Object(obj1, cube, red, metal, large)"])
    assert len(eng) == 1
    eng.add_facts(["Object(obj2, sphere, blue, rubber, small)"])
    assert len(eng) == 2
    assert eng.get_object_properties("obj1") is not None
    assert eng.get_object_properties("obj2") is not None


def test_add_facts_preserves_relations():
    eng = SimpleLogicEngine([
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, sphere, blue, rubber, small)",
        "Relation(obj1, left_of, obj2)",
    ])
    eng.add_facts(["Object(obj3, cylinder, green, metal, large)"])
    assert len(eng) == 3
    assert len(eng.get_all_relations()) == 1


def test_empty_engine():
    eng = SimpleLogicEngine()
    assert len(eng) == 0
    assert eng.find_objects_by_property("color", "red") == []
    assert eng.count_by_property("shape", "cube") == 0
    assert eng.get_all_relations() == []


def test_clear(engine):
    engine.clear()
    assert len(engine) == 0
    assert engine.get_all_relations() == []
