"""Pytest tests for SceneGraph."""

import pytest
from src.representation.scene_graph import (
    SceneGraph, Shape, Color, Material, Size, SpatialRelation, Position
)


def test_add_objects():
    scene = SceneGraph()
    id1 = scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    id2 = scene.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(2, 0, 0))
    id3 = scene.add_object(Shape.CYLINDER, Color.GREEN, Material.METAL, Size.LARGE, Position(1, 1, 0))
    assert len(scene) == 3
    assert id1 in scene
    assert id2 in scene
    assert id3 in scene


def test_add_duplicate_id_raises():
    scene = SceneGraph()
    scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0), obj_id="x")
    with pytest.raises(ValueError):
        scene.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(1, 0, 0), obj_id="x")


def test_add_relations():
    scene = SceneGraph()
    id1 = scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    id2 = scene.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(2, 0, 0))
    scene.add_relation(id1, SpatialRelation.LEFT_OF, id2)
    assert scene.relations[(id1, SpatialRelation.LEFT_OF, id2)] is True


def test_add_relation_missing_object_raises():
    scene = SceneGraph()
    id1 = scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    with pytest.raises(ValueError):
        scene.add_relation(id1, SpatialRelation.LEFT_OF, "nonexistent")


def test_predicate_format():
    scene = SceneGraph()
    cube_id = scene.add_object(
        Shape.CUBE, Color.RED, Material.METAL, Size.LARGE,
        Position(0, 0, 0), obj_id="red_cube"
    )
    sphere_id = scene.add_object(
        Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL,
        Position(2, 0, 0), obj_id="blue_sphere"
    )
    scene.add_relation(cube_id, SpatialRelation.LEFT_OF, sphere_id)

    predicates = scene.to_predicates()
    assert len(predicates) == 3
    assert "Object(red_cube, cube, red, metal, large)" in predicates
    assert "Object(blue_sphere, sphere, blue, rubber, small)" in predicates
    assert "Relation(red_cube, left_of, blue_sphere)" in predicates


def test_predicate_excludes_position():
    scene = SceneGraph()
    scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(3.5, 7.2, 1.1))
    predicates = scene.to_predicates()
    assert len(predicates) == 1
    assert "3.5" not in predicates[0]
    assert "7.2" not in predicates[0]


def test_predicate_excludes_false_relations():
    scene = SceneGraph()
    id1 = scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    id2 = scene.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(2, 0, 0))
    scene.add_relation(id1, SpatialRelation.LEFT_OF, id2, value=False)
    predicates = scene.to_predicates()
    assert not any("Relation" in p for p in predicates)


def test_object_filtering_by_color():
    scene = SceneGraph()
    scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    scene.add_object(Shape.CUBE, Color.BLUE, Material.METAL, Size.SMALL, Position(1, 0, 0))
    scene.add_object(Shape.SPHERE, Color.RED, Material.RUBBER, Size.LARGE, Position(2, 0, 0))
    scene.add_object(Shape.CYLINDER, Color.GREEN, Material.METAL, Size.SMALL, Position(3, 0, 0))

    assert len(scene.get_objects_by_property(color=Color.RED)) == 2
    assert len(scene.get_objects_by_property(material=Material.METAL)) == 3
    assert len(scene.get_objects_by_property(shape=Shape.CUBE, size=Size.LARGE)) == 1


def test_serialization_roundtrip():
    original = SceneGraph()
    id1 = original.add_object(
        Shape.CUBE, Color.RED, Material.METAL, Size.LARGE,
        Position(0.0, 0.0, 0.0), obj_id="test_cube"
    )
    id2 = original.add_object(
        Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL,
        Position(1.0, 1.0, 0.0), obj_id="test_sphere"
    )
    original.add_relation(id1, SpatialRelation.LEFT_OF, id2)

    restored = SceneGraph.from_dict(original.to_dict())

    assert set(restored.objects.keys()) == {"test_cube", "test_sphere"}
    assert restored.objects["test_cube"].shape == Shape.CUBE
    assert restored.objects["test_cube"].color == Color.RED
    assert restored.objects["test_sphere"].material == Material.RUBBER
    assert len([v for v in restored.relations.values() if v]) == 1
