#!/usr/bin/env python3
"""
Test script for QuestionParser class demonstrating natural language to structured query conversion.
"""

from src.language.question_parser import QuestionParser, QueryType, StructuredQuery


def test_property_queries():
    """Test property query parsing."""
    print("=== Testing Property Queries ===\n")
    
    parser = QuestionParser()
    
    property_questions = [
        "What color is the cube?",
        "What shape is the red object?",
        "What material is the blue sphere?",
        "What is the color of the red cube?",
        "What size is the metal cylinder?",
        "What color does the sphere have?"
    ]
    
    for question in property_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Property: {result.target_property}")
        print(f"  Value: {result.target_value}")
        print(f"  Object: {result.target_object}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def test_count_queries():
    """Test count query parsing."""
    print("=== Testing Count Queries ===\n")
    
    parser = QuestionParser()
    
    count_questions = [
        "How many red objects are there?",
        "Count the number of blue spheres",
        "How many objects are red?",
        "What is the total number of metal cubes?",
        "Count all large objects"
    ]
    
    for question in count_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Property: {result.target_property}")
        print(f"  Value: {result.target_value}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def test_relation_queries():
    """Test relation query parsing."""
    print("=== Testing Relation Queries ===\n")
    
    parser = QuestionParser()
    
    relation_questions = [
        "What is left of the blue sphere?",
        "What object is right of the red cube?",
        "Find the object that is above the green cylinder",
        "What is behind the yellow sphere?",
        "What object is to the left of the metal cube?",
        "Find objects that are below the large sphere"
    ]
    
    for question in relation_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Relation: {result.relation_type}")
        print(f"  Reference Object: {result.reference_object}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def test_existence_queries():
    """Test existence query parsing."""
    print("=== Testing Existence Queries ===\n")
    
    parser = QuestionParser()
    
    existence_questions = [
        "Are there any metal cubes?",
        "Is there a red sphere?",
        "Do any objects have red color?",
        "Are there any large metal objects?",
        "Is there a blue cylinder in the scene?"
    ]
    
    for question in existence_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Conditions: {result.conditions}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def test_comparison_queries():
    """Test comparison query parsing."""
    print("=== Testing Comparison Queries ===\n")
    
    parser = QuestionParser()
    
    comparison_questions = [
        "Compare obj1 and obj2",
        "What is the difference between red_cube and blue_sphere?",
        "Compare the properties of obj1 and obj3",
        "What are the similarities between obj2 and obj4?"
    ]
    
    for question in comparison_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Comparison Objects: {result.comparison_objects}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def test_integration_with_logic_engine():
    """Test integration with SimpleLogicEngine."""
    print("=== Testing Integration with Logic Engine ===\n")
    
    from src.reasoning.logic_engine import SimpleLogicEngine
    
    # Create sample facts
    facts = [
        "Object(red_cube, cube, red, metal, large)",
        "Object(blue_sphere, sphere, blue, rubber, small)",
        "Object(green_cylinder, cylinder, green, metal, large)",
        "Relation(red_cube, left_of, blue_sphere)",
        "Relation(green_cylinder, above, red_cube)"
    ]
    
    # Initialize components
    parser = QuestionParser()
    engine = SimpleLogicEngine(facts)
    
    # Test questions
    test_questions = [
        "What color is the cube?",
        "How many red objects are there?",
        "What is left of the blue sphere?",
        "Are there any metal cubes?"
    ]
    
    for question in test_questions:
        print(f"Question: '{question}'")
        
        # Parse question
        parsed = parser.parse(question)
        print(f"  Parsed Type: {parsed.query_type.value}")
        
        # Convert to logic query
        logic_query = parsed.to_logic_query()
        print(f"  Logic Query: '{logic_query}'")
        
        # Execute query
        result = engine.query(logic_query)
        print(f"  Result: {result}")
        print()


def test_error_handling():
    """Test error handling for unsupported questions."""
    print("=== Testing Error Handling ===\n")
    
    parser = QuestionParser()
    
    unsupported_questions = [
        "What is the meaning of life?",
        "How do I cook pasta?",
        "What time is it?",
        "Random text that doesn't make sense",
        "What is the weather like?"
    ]
    
    for question in unsupported_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Can Parse: {parser.validate_question(question)}")
        print()


def test_question_validation():
    """Test question validation functionality."""
    print("=== Testing Question Validation ===\n")
    
    parser = QuestionParser()
    
    # Valid questions
    valid_questions = [
        "What color is the cube?",
        "How many red objects are there?",
        "What is left of the blue sphere?",
        "Are there any metal cubes?"
    ]
    
    # Invalid questions
    invalid_questions = [
        "What is the meaning of life?",
        "How do I cook pasta?",
        "Random text"
    ]
    
    print("Valid questions:")
    for question in valid_questions:
        is_valid = parser.validate_question(question)
        print(f"  '{question}' -> {is_valid}")
    
    print("\nInvalid questions:")
    for question in invalid_questions:
        is_valid = parser.validate_question(question)
        print(f"  '{question}' -> {is_valid}")
    
    print()


def test_supported_question_types():
    """Test getting supported question types."""
    print("=== Testing Supported Question Types ===\n")
    
    parser = QuestionParser()
    supported_types = parser.get_supported_question_types()
    
    print("Supported question types:")
    for i, question_type in enumerate(supported_types, 1):
        print(f"  {i}. {question_type}")
    
    print()


def test_complex_parsing():
    """Test complex parsing scenarios."""
    print("=== Testing Complex Parsing Scenarios ===\n")
    
    parser = QuestionParser()
    
    complex_questions = [
        "What is the color of the large metal cube that is left of the blue sphere?",
        "How many small red objects are there in the scene?",
        "Find all objects that are above the red cube and have metal material",
        "What objects are both red and have cube shape?",
        "Count the number of objects that are either blue or green"
    ]
    
    for question in complex_questions:
        result = parser.parse(question)
        print(f"Question: '{question}'")
        print(f"  Type: {result.query_type.value}")
        print(f"  Logic Query: '{result.to_logic_query()}'")
        print()


def main():
    """Run all tests."""
    test_property_queries()
    test_count_queries()
    test_relation_queries()
    test_existence_queries()
    test_comparison_queries()
    test_integration_with_logic_engine()
    test_error_handling()
    test_question_validation()
    test_supported_question_types()
    test_complex_parsing()
    
    print("=== All Question Parser Tests Completed Successfully! ===")


if __name__ == "__main__":
    main()
