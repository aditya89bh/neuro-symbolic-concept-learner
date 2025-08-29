#!/usr/bin/env python3
"""
Test script for SceneGraph class demonstrating its functionality.
"""

from src.representation.scene_graph import (
    SceneGraph, Shape, Color, Material, Size, SpatialRelation, Position
)


def test_basic_functionality():
    """Test basic SceneGraph functionality."""
    print("=== Testing Basic SceneGraph Functionality ===\n")
    
    # Create a new scene graph
    scene = SceneGraph()
    
    # Add some objects
    obj1_id = scene.add_object(
        shape=Shape.CUBE,
        color=Color.RED,
        material=Material.METAL,
        size=Size.LARGE,
        position=Position(0.0, 0.0, 0.0)
    )
    
    obj2_id = scene.add_object(
        shape=Shape.SPHERE,
        color=Color.BLUE,
        material=Material.RUBBER,
        size=Size.SMALL,
        position=Position(2.0, 0.0, 0.0)
    )
    
    obj3_id = scene.add_object(
        shape=Shape.CYLINDER,
        color=Color.GREEN,
        material=Material.METAL,
        size=Size.LARGE,
        position=Position(1.0, 1.0, 0.0)
    )
    
    print(f"Added objects: {obj1_id}, {obj2_id}, {obj3_id}")
    print(f"Scene has {len(scene)} objects\n")
    
    # Add spatial relations
    scene.add_relation(obj1_id, SpatialRelation.LEFT_OF, obj2_id)
    scene.add_relation(obj3_id, SpatialRelation.ABOVE, obj1_id)
    scene.add_relation(obj2_id, SpatialRelation.RIGHT_OF, obj1_id)
    
    print("Added spatial relations:")
    for obj_id in [obj1_id, obj2_id, obj3_id]:
        relations = scene.get_relations(obj_id)
        print(f"  {obj_id}: {relations}")
    print()


def test_predicate_conversion():
    """Test conversion to logic programming predicates."""
    print("=== Testing Predicate Conversion ===\n")
    
    scene = SceneGraph()
    
    # Create a simple scene
    cube_id = scene.add_object(
        shape=Shape.CUBE,
        color=Color.RED,
        material=Material.METAL,
        size=Size.LARGE,
        position=Position(0.0, 0.0, 0.0),
        obj_id="red_cube"
    )
    
    sphere_id = scene.add_object(
        shape=Shape.SPHERE,
        color=Color.BLUE,
        material=Material.RUBBER,
        size=Size.SMALL,
        position=Position(2.0, 0.0, 0.0),
        obj_id="blue_sphere"
    )
    
    # Add relation
    scene.add_relation(cube_id, SpatialRelation.LEFT_OF, sphere_id)
    
    # Convert to predicates
    predicates = scene.to_predicates()
    
    print("Logic Programming Predicates:")
    for predicate in predicates:
        print(f"  {predicate}")
    print()


def test_object_filtering():
    """Test filtering objects by properties."""
    print("=== Testing Object Filtering ===\n")
    
    scene = SceneGraph()
    
    # Add various objects
    scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    scene.add_object(Shape.CUBE, Color.BLUE, Material.METAL, Size.SMALL, Position(1, 0, 0))
    scene.add_object(Shape.SPHERE, Color.RED, Material.RUBBER, Size.LARGE, Position(2, 0, 0))
    scene.add_object(Shape.CYLINDER, Color.GREEN, Material.METAL, Size.SMALL, Position(3, 0, 0))
    
    # Test different filters
    red_objects = scene.get_objects_by_property(color=Color.RED)
    metal_objects = scene.get_objects_by_property(material=Material.METAL)
    large_cubes = scene.get_objects_by_property(shape=Shape.CUBE, size=Size.LARGE)
    
    print(f"Red objects: {len(red_objects)}")
    for obj in red_objects:
        print(f"  {obj.obj_id}: {obj.shape.value} {obj.color.value}")
    
    print(f"\nMetal objects: {len(metal_objects)}")
    for obj in metal_objects:
        print(f"  {obj.obj_id}: {obj.shape.value} {obj.material.value}")
    
    print(f"\nLarge cubes: {len(large_cubes)}")
    for obj in large_cubes:
        print(f"  {obj.obj_id}: {obj.shape.value} {obj.size.value}")
    print()


def test_serialization():
    """Test serialization to/from dictionary."""
    print("=== Testing Serialization ===\n")
    
    # Create original scene
    original = SceneGraph()
    obj1 = original.add_object(
        shape=Shape.CUBE,
        color=Color.RED,
        material=Material.METAL,
        size=Size.LARGE,
        position=Position(0.0, 0.0, 0.0),
        obj_id="test_cube"
    )
    obj2 = original.add_object(
        shape=Shape.SPHERE,
        color=Color.BLUE,
        material=Material.RUBBER,
        size=Size.SMALL,
        position=Position(1.0, 1.0, 0.0),
        obj_id="test_sphere"
    )
    original.add_relation(obj1, SpatialRelation.LEFT_OF, obj2)
    
    # Serialize to dictionary
    data = original.to_dict()
    print("Serialized data:")
    print(f"  Objects: {list(data['objects'].keys())}")
    print(f"  Relations: {data['relations']}")
    
    # Deserialize back to SceneGraph
    restored = SceneGraph.from_dict(data)
    print(f"\nRestored scene: {restored}")
    print(f"Objects: {list(restored.objects.keys())}")
    print(f"Relations: {list(restored.relations.keys())}")
    print()


def main():
    """Run all tests."""
    test_basic_functionality()
    test_predicate_conversion()
    test_object_filtering()
    test_serialization()
    
    print("=== All Tests Completed Successfully! ===")


if __name__ == "__main__":
    main()
