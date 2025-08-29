"""
Question Parser for Natural Language to Structured Queries

This module provides a QuestionParser class that converts natural language questions
into structured query objects that can be processed by the SimpleLogicEngine.
It handles various CLEVR-style question types including property, count, relation,
and existence queries.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import re


class QueryType(Enum):
    """Types of queries that can be generated from questions."""
    PROPERTY = "property"
    COUNT = "count"
    RELATION = "relation"
    EXISTENCE = "existence"
    COMPARISON = "comparison"
    UNKNOWN = "unknown"


@dataclass
class StructuredQuery:
    """Structured representation of a parsed query."""
    query_type: QueryType
    target_property: Optional[str] = None
    target_value: Optional[str] = None
    target_object: Optional[str] = None
    relation_type: Optional[str] = None
    reference_object: Optional[str] = None
    comparison_objects: Optional[List[str]] = None
    conditions: Optional[Dict[str, str]] = None
    raw_question: Optional[str] = None
    
    def to_logic_query(self) -> str:
        """Convert structured query to a logic engine query string."""
        if self.query_type == QueryType.PROPERTY:
            if self.target_property and self.target_object:
                return f"find objects where {self.target_property} is {self.target_value}"
            elif self.target_value:
                return f"find {self.target_value} objects"
        
        elif self.query_type == QueryType.COUNT:
            if self.target_value and self.target_property:
                return f"how many {self.target_value} {self.target_property}"
            elif self.target_value:
                return f"count objects where {self.target_property} is {self.target_value}"
        
        elif self.query_type == QueryType.RELATION:
            if self.relation_type and self.reference_object:
                return f"find objects {self.relation_type} {self.reference_object}"
            elif self.target_object and self.reference_object:
                return f"find relations between {self.target_object} and {self.reference_object}"
        
        elif self.query_type == QueryType.EXISTENCE:
            if self.conditions:
                conditions_str = " and ".join([f"{k} is {v}" for k, v in self.conditions.items()])
                return f"find objects where {conditions_str}"
        
        elif self.query_type == QueryType.COMPARISON:
            if self.comparison_objects and len(self.comparison_objects) >= 2:
                return f"compare {' and '.join(self.comparison_objects)}"
        
        return self.raw_question or ""


class QuestionParser:
    """
    A parser that converts natural language questions into structured queries.
    
    This class handles various CLEVR-style question patterns and converts them
    into structured query objects that can be processed by the SimpleLogicEngine.
    
    Attributes:
        property_keywords: Keywords that indicate property queries
        count_keywords: Keywords that indicate count queries
        relation_keywords: Keywords that indicate relation queries
        existence_keywords: Keywords that indicate existence queries
        comparison_keywords: Keywords that indicate comparison queries
    """
    
    def __init__(self):
        """Initialize the question parser with keyword mappings."""
        # Property query patterns
        self.property_keywords = {
            'color': ['color', 'colour', 'colored', 'coloured'],
            'shape': ['shape', 'form', 'type'],
            'material': ['material', 'made of', 'substance'],
            'size': ['size', 'big', 'small', 'large', 'tiny']
        }
        
        # Count query patterns
        self.count_keywords = [
            'how many', 'count', 'number of', 'amount of', 'total'
        ]
        
        # Relation query patterns
        self.relation_keywords = {
            'left_of': ['left of', 'to the left of', 'on the left side of'],
            'right_of': ['right of', 'to the right of', 'on the right side of'],
            'above': ['above', 'over', 'on top of', 'higher than'],
            'below': ['below', 'under', 'beneath', 'lower than'],
            'behind': ['behind', 'in back of', 'at the back of'],
            'front_of': ['front of', 'in front of', 'ahead of'],
            'same_x': ['same x', 'same horizontal position'],
            'same_y': ['same y', 'same vertical position'],
            'same_z': ['same z', 'same depth']
        }
        
        # Existence query patterns
        self.existence_keywords = [
            'are there', 'is there', 'exist', 'any', 'some'
        ]
        
        # Comparison query patterns
        self.comparison_keywords = [
            'compare', 'same', 'different', 'similar', 'difference between'
        ]
        
        # Object property values
        self.valid_values = {
            'color': ['red', 'blue', 'green', 'yellow', 'purple', 'cyan', 'brown', 'gray'],
            'shape': ['cube', 'sphere', 'cylinder'],
            'material': ['metal', 'rubber'],
            'size': ['small', 'large']
        }
    
    def parse(self, question: str) -> StructuredQuery:
        """
        Parse a natural language question into a structured query.
        
        Args:
            question: The natural language question to parse
            
        Returns:
            StructuredQuery object representing the parsed question
            
        Raises:
            ValueError: If the question cannot be parsed
        """
        question = question.strip().lower()
        
        # Try to identify query type and parse accordingly
        if self._is_property_query(question):
            return self._parse_property_query(question)
        elif self._is_count_query(question):
            return self._parse_count_query(question)
        elif self._is_relation_query(question):
            return self._parse_relation_query(question)
        elif self._is_existence_query(question):
            return self._parse_existence_query(question)
        elif self._is_comparison_query(question):
            return self._parse_comparison_query(question)
        else:
            return StructuredQuery(
                query_type=QueryType.UNKNOWN,
                raw_question=question
            )
    
    def _is_property_query(self, question: str) -> bool:
        """Check if the question is asking about object properties."""
        # Patterns like "What color is...", "What shape is...", etc.
        property_patterns = [
            r'what\s+(color|shape|material|size)\s+is',
            r'what\s+is\s+the\s+(color|shape|material|size)\s+of',
            r'what\s+(color|shape|material|size)\s+does\s+\w+\s+have'
        ]
        
        for pattern in property_patterns:
            if re.search(pattern, question):
                return True
        
        # Check for direct property mentions
        for property_name in self.property_keywords.keys():
            if property_name in question:
                return True
        
        return False
    
    def _parse_property_query(self, question: str) -> StructuredQuery:
        """Parse a property query question."""
        # Extract property being asked about
        target_property = None
        target_value = None
        target_object = None
        
        # Pattern: "What color is the cube?"
        match = re.search(r'what\s+(\w+)\s+is\s+(?:the\s+)?(\w+)', question)
        if match:
            target_property = match.group(1)
            target_object = match.group(2)
        
        # Pattern: "What is the color of the red cube?"
        match = re.search(r'what\s+is\s+the\s+(\w+)\s+of\s+(?:the\s+)?(\w+)\s+(\w+)', question)
        if match:
            target_property = match.group(1)
            target_value = match.group(2)
            target_object = match.group(3)
        
        # Pattern: "What color is the red cube?"
        match = re.search(r'what\s+(\w+)\s+is\s+(?:the\s+)?(\w+)\s+(\w+)', question)
        if match:
            target_property = match.group(1)
            target_value = match.group(2)
            target_object = match.group(3)
        
        # If no specific object mentioned, try to extract from context
        if not target_object:
            # Look for object descriptions in the question
            for value in self.valid_values.get(target_property, []):
                if value in question:
                    target_value = value
                    break
        
        return StructuredQuery(
            query_type=QueryType.PROPERTY,
            target_property=target_property,
            target_value=target_value,
            target_object=target_object,
            raw_question=question
        )
    
    def _is_count_query(self, question: str) -> bool:
        """Check if the question is asking for a count."""
        for keyword in self.count_keywords:
            if keyword in question:
                return True
        return False
    
    def _parse_count_query(self, question: str) -> StructuredQuery:
        """Parse a count query question."""
        target_property = None
        target_value = None
        
        # Pattern: "How many red objects are there?"
        match = re.search(r'how\s+many\s+(\w+)\s+(\w+)', question)
        if match:
            target_value = match.group(1)
            target_property = match.group(2)
        
        # Pattern: "Count the number of blue spheres"
        match = re.search(r'count\s+(?:the\s+number\s+of\s+)?(\w+)\s+(\w+)', question)
        if match:
            target_value = match.group(1)
            target_property = match.group(2)
        
        # Pattern: "How many objects are red?"
        match = re.search(r'how\s+many\s+objects\s+are\s+(\w+)', question)
        if match:
            target_value = match.group(1)
            # Try to determine property from value
            target_property = self._infer_property_from_value(target_value)
        
        return StructuredQuery(
            query_type=QueryType.COUNT,
            target_property=target_property,
            target_value=target_value,
            raw_question=question
        )
    
    def _is_relation_query(self, question: str) -> bool:
        """Check if the question is asking about spatial relations."""
        # Check for relation keywords
        for relation_type, keywords in self.relation_keywords.items():
            for keyword in keywords:
                if keyword in question:
                    return True
        
        # Check for relation patterns
        relation_patterns = [
            r'what\s+is\s+(?:to\s+)?(?:the\s+)?(left|right|above|below|behind|front)\s+of',
            r'what\s+(?:object\s+)?is\s+(?:to\s+)?(?:the\s+)?(left|right|above|below|behind|front)\s+of',
            r'find\s+(?:the\s+)?(?:object\s+)?(?:that\s+)?is\s+(?:to\s+)?(?:the\s+)?(left|right|above|below|behind|front)\s+of'
        ]
        
        for pattern in relation_patterns:
            if re.search(pattern, question):
                return True
        
        return False
    
    def _parse_relation_query(self, question: str) -> StructuredQuery:
        """Parse a relation query question."""
        relation_type = None
        reference_object = None
        
        # Pattern: "What is left of the blue sphere?"
        match = re.search(r'what\s+is\s+(?:to\s+)?(?:the\s+)?(\w+)\s+of\s+(?:the\s+)?(\w+)\s+(\w+)', question)
        if match:
            relation_type = match.group(1)
            reference_object = f"{match.group(2)}_{match.group(3)}"
        
        # Pattern: "What object is left of the blue sphere?"
        match = re.search(r'what\s+(?:object\s+)?is\s+(?:to\s+)?(?:the\s+)?(\w+)\s+of\s+(?:the\s+)?(\w+)\s+(\w+)', question)
        if match:
            relation_type = match.group(1)
            reference_object = f"{match.group(2)}_{match.group(3)}"
        
        # Pattern: "Find the object that is left of the blue sphere"
        match = re.search(r'find\s+(?:the\s+)?(?:object\s+)?(?:that\s+)?is\s+(?:to\s+)?(?:the\s+)?(\w+)\s+of\s+(?:the\s+)?(\w+)\s+(\w+)', question)
        if match:
            relation_type = match.group(1)
            reference_object = f"{match.group(2)}_{match.group(3)}"
        
        # Normalize relation type
        if relation_type:
            relation_type = self._normalize_relation_type(relation_type)
        
        return StructuredQuery(
            query_type=QueryType.RELATION,
            relation_type=relation_type,
            reference_object=reference_object,
            raw_question=question
        )
    
    def _is_existence_query(self, question: str) -> bool:
        """Check if the question is asking about existence."""
        for keyword in self.existence_keywords:
            if keyword in question:
                return True
        return False
    
    def _parse_existence_query(self, question: str) -> StructuredQuery:
        """Parse an existence query question."""
        conditions = {}
        
        # Pattern: "Are there any metal cubes?"
        match = re.search(r'are\s+there\s+any\s+(\w+)\s+(\w+)', question)
        if match:
            material = match.group(1)
            shape = match.group(2)
            conditions['material'] = material
            conditions['shape'] = shape
        
        # Pattern: "Is there a red sphere?"
        match = re.search(r'is\s+there\s+(?:a\s+)?(\w+)\s+(\w+)', question)
        if match:
            color = match.group(1)
            shape = match.group(2)
            conditions['color'] = color
            conditions['shape'] = shape
        
        # Pattern: "Do any objects have property value?"
        match = re.search(r'do\s+any\s+objects\s+have\s+(\w+)\s+(\w+)', question)
        if match:
            property_name = match.group(1)
            value = match.group(2)
            conditions[property_name] = value
        
        return StructuredQuery(
            query_type=QueryType.EXISTENCE,
            conditions=conditions,
            raw_question=question
        )
    
    def _is_comparison_query(self, question: str) -> bool:
        """Check if the question is asking for a comparison."""
        for keyword in self.comparison_keywords:
            if keyword in question:
                return True
        return False
    
    def _parse_comparison_query(self, question: str) -> StructuredQuery:
        """Parse a comparison query question."""
        comparison_objects = []
        
        # Pattern: "Compare obj1 and obj2"
        match = re.search(r'compare\s+(\w+)\s+and\s+(\w+)', question)
        if match:
            comparison_objects = [match.group(1), match.group(2)]
        
        # Pattern: "What is the difference between obj1 and obj2"
        match = re.search(r'difference\s+between\s+(\w+)\s+and\s+(\w+)', question)
        if match:
            comparison_objects = [match.group(1), match.group(2)]
        
        return StructuredQuery(
            query_type=QueryType.COMPARISON,
            comparison_objects=comparison_objects,
            raw_question=question
        )
    
    def _infer_property_from_value(self, value: str) -> Optional[str]:
        """Infer the property type from a value."""
        for property_name, valid_values in self.valid_values.items():
            if value in valid_values:
                return property_name
        return None
    
    def _normalize_relation_type(self, relation: str) -> str:
        """Normalize relation type to standard format."""
        relation_mapping = {
            'left': 'left_of',
            'right': 'right_of',
            'above': 'above',
            'below': 'below',
            'behind': 'behind',
            'front': 'front_of'
        }
        return relation_mapping.get(relation, relation)
    
    def get_supported_question_types(self) -> List[str]:
        """Get a list of supported question types."""
        return [
            "Property queries (What color is the cube?)",
            "Count queries (How many red objects are there?)",
            "Relation queries (What is left of the blue sphere?)",
            "Existence queries (Are there any metal cubes?)",
            "Comparison queries (Compare obj1 and obj2)"
        ]
    
    def validate_question(self, question: str) -> bool:
        """
        Validate if a question can be parsed.
        
        Args:
            question: The question to validate
            
        Returns:
            True if the question can be parsed, False otherwise
        """
        try:
            parsed = self.parse(question)
            return parsed.query_type != QueryType.UNKNOWN
        except:
            return False
    
    def __str__(self) -> str:
        """String representation of the question parser."""
        return "QuestionParser()"
    
    def __repr__(self) -> str:
        """Detailed string representation of the question parser."""
        return "QuestionParser()"
