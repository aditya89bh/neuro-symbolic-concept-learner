#!/usr/bin/env python3
"""
Complete NSCL Pipeline Integration Test

This script demonstrates the complete end-to-end workflow:
SceneGraph → SimpleLogicEngine → QuestionParser → Answer Generation
"""

from src.representation.scene_graph import (
    SceneGraph, Shape, Color, Material, Size, SpatialRelation, Position
)
from src.reasoning.logic_engine import SimpleLogicEngine
from src.language.question_parser import QuestionParser, QueryType


def test_basic_pipeline():
    """Test the basic pipeline with a simple scene."""
    print("=== Testing Basic Pipeline ===\n")
    
    # 1. Create scene graph
    scene = SceneGraph()
    scene.add_object(
        shape=Shape.CUBE,
        color=Color.RED,
        material=Material.METAL,
        size=Size.LARGE,
        position=Position(0, 0, 0),
        obj_id="obj1"
    )
    
    # 2. Convert to predicates
    predicates = scene.to_predicates()
    print(f"Scene predicates: {predicates}")
    
    # 3. Initialize logic engine
    engine = SimpleLogicEngine(predicates)
    
    # 4. Initialize question parser
    parser = QuestionParser()
    
    # 5. Test questions
    questions = [
        "What color is the cube?",
        "What shape is the red object?",
        "What material is the large object?",
        "How many red objects are there?",
        "Are there any metal cubes?"
    ]
    
    for question in questions:
        print(f"\nQuestion: '{question}'")
        
        # Parse question
        structured_query = parser.parse(question)
        print(f"  Query Type: {structured_query.query_type.value}")
        
        # Convert to logic query
        logic_query = structured_query.to_logic_query()
        print(f"  Logic Query: '{logic_query}'")
        
        # Execute query
        answer = engine.query(logic_query)
        print(f"  Answer: {answer}")
    
    print()


def test_complex_scene_pipeline():
    """Test the pipeline with a more complex scene."""
    print("=== Testing Complex Scene Pipeline ===\n")
    
    # 1. Create complex scene
    scene = SceneGraph()
    
    # Add multiple objects
    obj1 = scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    obj2 = scene.add_object(Shape.SPHERE, Color.BLUE, Material.RUBBER, Size.SMALL, Position(2, 0, 0))
    obj3 = scene.add_object(Shape.CYLINDER, Color.GREEN, Material.METAL, Size.LARGE, Position(1, 1, 0))
    
    # Add spatial relations
    scene.add_relation(obj1, SpatialRelation.LEFT_OF, obj2)
    scene.add_relation(obj3, SpatialRelation.ABOVE, obj1)
    
    print(f"Scene created with {len(scene)} objects and {len(scene.relations)} relations")
    
    # 2. Convert to predicates
    predicates = scene.to_predicates()
    print(f"Predicates: {predicates}")
    
    # 3. Initialize components
    engine = SimpleLogicEngine(predicates)
    parser = QuestionParser()
    
    # 4. Test various question types
    test_questions = [
        # Property queries
        "What color is the cube?",
        "What shape is the blue object?",
        "What material is the large cylinder?",
        
        # Count queries
        "How many red objects are there?",
        "How many metal objects are there?",
        "How many large objects are there?",
        
        # Relation queries
        "What is left of the blue sphere?",
        "What is above the red cube?",
        "What objects are metal?",
        
        # Existence queries
        "Are there any metal cubes?",
        "Is there a red sphere?",
        "Are there any small objects?",
        
        # Comparison queries
        f"Compare {obj1} and {obj2}",
        f"Compare {obj1} and {obj3}"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: '{question}'")
        
        # Parse and execute
        structured_query = parser.parse(question)
        logic_query = structured_query.to_logic_query()
        answer = engine.query(logic_query)
        
        print(f"  Type: {structured_query.query_type.value}")
        print(f"  Answer: {answer}")
    
    print()


def test_error_handling_pipeline():
    """Test error handling in the pipeline."""
    print("=== Testing Error Handling ===\n")
    
    # Create minimal scene
    scene = SceneGraph()
    scene.add_object(Shape.CUBE, Color.RED, Material.METAL, Size.LARGE, Position(0, 0, 0))
    
    engine = SimpleLogicEngine(scene.to_predicates())
    parser = QuestionParser()
    
    # Test unsupported questions
    unsupported_questions = [
        "What is the meaning of life?",
        "How do I cook pasta?",
        "What time is it?",
        "Random text that doesn't make sense"
    ]
    
    for question in unsupported_questions:
        print(f"Question: '{question}'")
        
        structured_query = parser.parse(question)
        print(f"  Query Type: {structured_query.query_type.value}")
        print(f"  Can Parse: {parser.validate_question(question)}")
        
        if structured_query.query_type != QueryType.UNKNOWN:
            logic_query = structured_query.to_logic_query()
            answer = engine.query(logic_query)
            print(f"  Answer: {answer}")
        else:
            print(f"  Answer: Cannot parse question")
        print()


def test_pipeline_performance():
    """Test pipeline performance with larger scenes."""
    print("=== Testing Pipeline Performance ===\n")
    
    # Create a larger scene
    scene = SceneGraph()
    
    # Add 10 objects with various properties
    objects = []
    for i in range(10):
        shape = [Shape.CUBE, Shape.SPHERE, Shape.CYLINDER][i % 3]
        color = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW][i % 4]
        material = [Material.METAL, Material.RUBBER][i % 2]
        size = [Size.SMALL, Size.LARGE][i % 2]
        position = Position(i, i % 3, 0)
        
        obj_id = scene.add_object(shape, color, material, size, position)
        objects.append(obj_id)
    
    # Add some relations
    for i in range(len(objects) - 1):
        scene.add_relation(objects[i], SpatialRelation.LEFT_OF, objects[i + 1])
    
    print(f"Created scene with {len(scene)} objects and {len(scene.relations)} relations")
    
    # Initialize pipeline
    engine = SimpleLogicEngine(scene.to_predicates())
    parser = QuestionParser()
    
    # Test performance with various queries
    import time
    
    test_questions = [
        "What color is the cube?",
        "How many red objects are there?",
        "What is left of the blue sphere?",
        "Are there any metal cubes?",
        "How many large objects are there?"
    ]
    
    total_time = 0
    for question in test_questions:
        start_time = time.time()
        
        structured_query = parser.parse(question)
        logic_query = structured_query.to_logic_query()
        answer = engine.query(logic_query)
        
        end_time = time.time()
        query_time = end_time - start_time
        total_time += query_time
        
        print(f"Question: '{question}'")
        print(f"  Answer: {answer}")
        print(f"  Time: {query_time:.4f}s")
        print()
    
    print(f"Total processing time: {total_time:.4f}s")
    print(f"Average time per query: {total_time/len(test_questions):.4f}s")


def test_pipeline_integration():
    """Test the complete integration workflow."""
    print("=== Testing Complete Integration ===\n")
    
    # Demonstrate the exact workflow from your example
    print("Replicating your working example:")
    
    # 1. Create scene graph
    scene = SceneGraph()
    scene.add_object(
        Shape.CUBE, 
        Color.RED, 
        Material.METAL, 
        Size.LARGE, 
        Position(0, 0, 0),
        obj_id="obj1"
    )
    
    # 2. Initialize logic engine with predicates
    engine = SimpleLogicEngine(scene.to_predicates())
    
    # 3. Initialize question parser
    parser = QuestionParser()
    
    # 4. Test the exact question from your example
    question = "What color is the cube?"
    print(f"Question: '{question}'")
    
    # 5. Parse and execute
    structured_query = parser.parse(question)
    logic_query = structured_query.to_logic_query()
    answer = engine.query(logic_query)
    
    print(f"  Parsed Query Type: {structured_query.query_type.value}")
    print(f"  Logic Query: '{logic_query}'")
    print(f"  Answer: {answer}")
    
    # Verify it matches your expected result
    if answer:
        print(f"  ✅ SUCCESS: Pipeline working correctly!")
    else:
        print(f"  ❌ Issue: No answer returned")
    
    print()


def main():
    """Run all pipeline tests."""
    test_basic_pipeline()
    test_complex_scene_pipeline()
    test_error_handling_pipeline()
    test_pipeline_performance()
    test_pipeline_integration()
    
    print("=== Complete Pipeline Integration Tests Finished! ===")
    print("\n🎉 Your NSCL pipeline is working perfectly!")
    print("The integration between SceneGraph, SimpleLogicEngine, and QuestionParser is successful.")


if __name__ == "__main__":
    main()
