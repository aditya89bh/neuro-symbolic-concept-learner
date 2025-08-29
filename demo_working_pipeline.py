#!/usr/bin/env python3
"""
Demonstration of the Working NSCL Pipeline

This script replicates the exact working example provided by the user.
"""

from src.representation.scene_graph import (
    SceneGraph, Shape, Color, Material, Size, Position
)
from src.reasoning.logic_engine import SimpleLogicEngine
from src.language.question_parser import QuestionParser


def demo_working_pipeline():
    """Demonstrate the working pipeline exactly as shown in the user's example."""
    print("=== Working NSCL Pipeline Demonstration ===\n")
    
    # 1. Create scene graph (exactly as in your example)
    scene = SceneGraph()
    scene.add_object(
        Shape.CUBE, 
        Color.RED, 
        Material.METAL, 
        Size.LARGE, 
        Position(0, 0, 0),
        obj_id="obj1"
    )
    
    print("✅ Scene created with red metal large cube")
    
    # 2. Convert to predicates
    predicates = scene.to_predicates()
    print(f"✅ Predicates: {predicates}")
    
    # 3. Initialize logic engine with predicates
    engine = SimpleLogicEngine(predicates)
    print("✅ Logic engine initialized")
    
    # 4. Initialize question parser
    parser = QuestionParser()
    print("✅ Question parser initialized")
    
    # 5. Test the exact question from your example
    question = "What color is the cube?"
    print(f"\n🔍 Question: '{question}'")
    
    # 6. Parse question
    structured_query = parser.parse(question)
    print(f"✅ Parsed query type: {structured_query.query_type.value}")
    
    # 7. Convert to logic query
    logic_query = structured_query.to_logic_query()
    print(f"✅ Logic query: '{logic_query}'")
    
    # 8. Execute query
    answer = engine.query(logic_query)
    print(f"✅ Answer: {answer}")
    
    # 9. Test additional questions to show the pipeline working
    additional_questions = [
        "How many red objects are there?",
        "Are there any metal cubes?",
        "What shape is the red object?",
        "What material is the large object?"
    ]
    
    print(f"\n=== Testing Additional Questions ===")
    for question in additional_questions:
        print(f"\n🔍 Question: '{question}'")
        
        structured_query = parser.parse(question)
        logic_query = structured_query.to_logic_query()
        answer = engine.query(logic_query)
        
        print(f"✅ Type: {structured_query.query_type.value}")
        print(f"✅ Answer: {answer}")
    
    print(f"\n🎉 Pipeline demonstration completed successfully!")


def demo_direct_logic_engine():
    """Demonstrate direct logic engine usage for comparison."""
    print("\n=== Direct Logic Engine Usage (for comparison) ===")
    
    # Create facts directly
    facts = [
        "Object(obj1, cube, red, metal, large)"
    ]
    
    engine = SimpleLogicEngine(facts)
    
    # Test direct queries
    direct_queries = [
        "find red objects",
        "find objects where shape is cube",
        "find objects where color is red",
        "how many red objects"
    ]
    
    for query in direct_queries:
        result = engine.query(query)
        print(f"Query: '{query}' -> {result}")


if __name__ == "__main__":
    demo_working_pipeline()
    demo_direct_logic_engine()
