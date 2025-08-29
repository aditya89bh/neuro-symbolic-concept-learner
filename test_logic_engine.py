#!/usr/bin/env python3
"""
Test script for SimpleLogicEngine class demonstrating CLEVR-style query handling.
"""

from src.reasoning.logic_engine import SimpleLogicEngine


def test_basic_queries():
    """Test basic query functionality."""
    print("=== Testing Basic Queries ===\n")
    
    # Create sample facts from a CLEVR scene
    facts = [
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, sphere, blue, rubber, small)",
        "Object(obj3, cylinder, green, metal, large)",
        "Object(obj4, cube, yellow, rubber, small)",
        "Relation(obj1, left_of, obj2)",
        "Relation(obj3, above, obj1)",
        "Relation(obj4, right_of, obj2)"
    ]
    
    # Initialize logic engine
    engine = SimpleLogicEngine(facts)
    print(f"Initialized engine with {len(engine)} objects and {len(engine.get_all_relations())} relations\n")
    
    # Test find queries
    print("Find queries:")
    queries = [
        "find objects where shape is cube",
        "find red objects",
        "find metal objects",
        "find large objects"
    ]
    
    for query in queries:
        result = engine.query(query)
        print(f"  '{query}' -> {result}")
    
    print()
    
    # Test count queries
    print("Count queries:")
    count_queries = [
        "count objects where shape is cube",
        "how many red objects",
        "count objects where material is metal",
        "how many large objects"
    ]
    
    for query in count_queries:
        result = engine.query(query)
        print(f"  '{query}' -> {result}")
    
    print()


def test_relation_queries():
    """Test relation-based queries."""
    print("=== Testing Relation Queries ===\n")
    
    facts = [
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, sphere, blue, rubber, small)",
        "Object(obj3, cylinder, green, metal, large)",
        "Relation(obj1, left_of, obj2)",
        "Relation(obj3, above, obj1)",
        "Relation(obj2, right_of, obj1)"
    ]
    
    engine = SimpleLogicEngine(facts)
    
    # Test relation queries
    print("Relation queries:")
    queries = [
        "find relations between obj1 and obj2",
        "find objects left_of obj1",
        "find objects above obj1"
    ]
    
    for query in queries:
        result = engine.query(query)
        print(f"  '{query}' -> {result}")
    
    print()


def test_comparison_queries():
    """Test object comparison queries."""
    print("=== Testing Comparison Queries ===\n")
    
    facts = [
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, sphere, blue, rubber, small)",
        "Object(obj3, cube, red, metal, small)"
    ]
    
    engine = SimpleLogicEngine(facts)
    
    # Test comparison queries
    print("Comparison queries:")
    queries = [
        "compare obj1 and obj2",
        "compare obj1 and obj3"
    ]
    
    for query in queries:
        result = engine.query(query)
        print(f"  '{query}' -> {result}")
        if isinstance(result, dict) and 'similarities' in result:
            print(f"    Similarities: {result['similarities']}")
            print(f"    Differences: {result['differences']}")
        print()


def test_direct_methods():
    """Test direct method calls."""
    print("=== Testing Direct Methods ===\n")
    
    facts = [
        "Object(obj1, cube, red, metal, large)",
        "Object(obj2, sphere, blue, rubber, small)",
        "Object(obj3, cylinder, green, metal, large)",
        "Relation(obj1, left_of, obj2)"
    ]
    
    engine = SimpleLogicEngine(facts)
    
    # Test direct method calls
    print("Direct method calls:")
    
    # Find objects by property
    red_objects = engine.find_objects_by_property("color", "red")
    print(f"  find_objects_by_property('color', 'red') -> {red_objects}")
    
    metal_objects = engine.find_objects_by_property("material", "metal")
    print(f"  find_objects_by_property('material', 'metal') -> {metal_objects}")
    
    # Count by property
    cube_count = engine.count_by_property("shape", "cube")
    print(f"  count_by_property('shape', 'cube') -> {cube_count}")
    
    # Get object properties
    obj1_props = engine.get_object_properties("obj1")
    print(f"  get_object_properties('obj1') -> {obj1_props}")
    
    # Find relations
    relations = engine.find_relations_between("obj1", "obj2")
    print(f"  find_relations_between('obj1', 'obj2') -> {relations}")
    
    print()


def test_complex_scenarios():
    """Test more complex CLEVR-style scenarios."""
    print("=== Testing Complex Scenarios ===\n")
    
    # More complex scene with multiple objects and relations
    facts = [
        "Object(red_cube, cube, red, metal, large)",
        "Object(blue_sphere, sphere, blue, rubber, small)",
        "Object(green_cylinder, cylinder, green, metal, large)",
        "Object(yellow_cube, cube, yellow, rubber, small)",
        "Object(purple_sphere, sphere, purple, metal, small)",
        "Relation(red_cube, left_of, blue_sphere)",
        "Relation(green_cylinder, above, red_cube)",
        "Relation(yellow_cube, right_of, blue_sphere)",
        "Relation(purple_sphere, behind, green_cylinder)"
    ]
    
    engine = SimpleLogicEngine(facts)
    
    print("Complex scene queries:")
    
    # Multi-step reasoning scenarios
    scenarios = [
        "find objects where shape is cube and color is red",
        "count objects where material is metal and size is large",
        "find objects where shape is sphere and material is rubber",
        "how many small objects",
        "find objects where color is blue or green"
    ]
    
    for scenario in scenarios:
        result = engine.query(scenario)
        print(f"  '{scenario}' -> {result}")
    
    print()


def test_error_handling():
    """Test error handling and edge cases."""
    print("=== Testing Error Handling ===\n")
    
    # Test with empty engine
    empty_engine = SimpleLogicEngine()
    print("Empty engine tests:")
    print(f"  query('find red objects') -> {empty_engine.query('find red objects')}")
    print(f"  count_by_property('color', 'red') -> {empty_engine.count_by_property('color', 'red')}")
    
    # Test with invalid queries
    facts = ["Object(obj1, cube, red, metal, large)"]
    engine = SimpleLogicEngine(facts)
    
    print("\nInvalid query tests:")
    invalid_queries = [
        "find objects where invalid_property is value",
        "count objects where shape is nonexistent",
        "compare obj1 and nonexistent_obj"
    ]
    
    for query in invalid_queries:
        result = engine.query(query)
        print(f"  '{query}' -> {result}")
    
    print()


def main():
    """Run all tests."""
    test_basic_queries()
    test_relation_queries()
    test_comparison_queries()
    test_direct_methods()
    test_complex_scenarios()
    test_error_handling()
    
    print("=== All Logic Engine Tests Completed Successfully! ===")


if __name__ == "__main__":
    main()
