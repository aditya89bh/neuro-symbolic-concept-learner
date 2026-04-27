"""
Simple Logic Engine for CLEVR-style Reasoning

This module provides a SimpleLogicEngine class that can process predicate strings
and answer basic queries about objects and their properties. It's designed to handle
CLEVR-style questions using simple string parsing and matching.
"""

from typing import Dict, List, Optional, Set, Tuple, Union, Any
import re
from enum import Enum


class QueryType(Enum):
    """Types of queries the logic engine can handle."""
    FIND_BY_PROPERTY = "find_by_property"
    COUNT_OBJECTS = "count_objects"
    FIND_RELATIONS = "find_relations"
    COMPARE_OBJECTS = "compare_objects"
    SPATIAL_QUERY = "spatial_query"


class SimpleLogicEngine:
    """
    A simple logic engine that processes predicate strings and answers queries.
    
    This engine can handle basic CLEVR-style questions by parsing predicate strings
    and performing simple string matching and property filtering operations.
    
    Attributes:
        facts: List of predicate strings representing the knowledge base
        objects: Dictionary mapping object IDs to their properties
        relations: List of relation predicates
    """
    
    def __init__(self, facts: Optional[List[str]] = None):
        """
        Initialize the logic engine with optional facts.
        
        Args:
            facts: List of predicate strings to initialize the knowledge base
        """
        self.facts: List[str] = facts or []
        self.objects: Dict[str, Dict[str, str]] = {}
        self.relations: List[Tuple[str, str, str]] = []  # (obj1, relation, obj2)
        self._parse_facts()
    
    def add_facts(self, facts: List[str]) -> None:
        """
        Add new facts to the knowledge base.

        Args:
            facts: List of predicate strings to add
        """
        self.facts.extend(facts)
        for fact in facts:
            self._parse_predicate(fact)
    
    def _parse_facts(self) -> None:
        """Parse all facts to extract objects and relations."""
        self.objects.clear()
        self.relations.clear()
        
        for fact in self.facts:
            self._parse_predicate(fact)
    
    def _parse_predicate(self, predicate: str) -> None:
        """
        Parse a single predicate string.
        
        Args:
            predicate: Predicate string to parse
        """
        # Remove whitespace and parentheses
        predicate = predicate.strip()
        
        # Parse Object predicates: Object(obj_id, shape, color, material, size)
        object_match = re.match(r'Object\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', predicate)
        if object_match:
            obj_id, shape, color, material, size = object_match.groups()
            self.objects[obj_id.strip()] = {
                'shape': shape.strip(),
                'color': color.strip(),
                'material': material.strip(),
                'size': size.strip()
            }
            return
        
        # Parse Relation predicates: Relation(obj1, relation, obj2)
        relation_match = re.match(r'Relation\(([^,]+),\s*([^,]+),\s*([^)]+)\)', predicate)
        if relation_match:
            obj1, relation, obj2 = relation_match.groups()
            self.relations.append((
                obj1.strip(),
                relation.strip(),
                obj2.strip()
            ))
            return
    
    def query(self, query: str) -> Union[List[str], int, List[Tuple[str, str, str]], Dict[str, Any]]:
        """
        Process a natural language query and return results.
        
        Args:
            query: Natural language query string
            
        Returns:
            Query results (varies by query type)
        """
        query = query.lower().strip()
        
        # Handle different query patterns
        if "find" in query and "where" in query:
            return self._handle_find_query(query)
        elif "count" in query or "how many" in query:
            return self._handle_count_query(query)
        elif "relation" in query or "between" in query:
            return self._handle_relation_query(query)
        elif "compare" in query or "same" in query or "different" in query:
            return self._handle_compare_query(query)
        else:
            return self._handle_general_query(query)
    
    def _handle_find_query(self, query: str) -> List[str]:
        """Handle 'find objects where property is value' queries."""
        # Extract property and value from query
        # Pattern: "find objects where [property] is [value]"
        match = re.search(r'where\s+(\w+)\s+is\s+(\w+)', query)
        if match:
            property_name, value = match.groups()
            return self.find_objects_by_property(property_name, value)
        
        # Pattern: "find [value] [property] objects"
        match = re.search(r'find\s+(\w+)\s+(\w+)', query)
        if match:
            value, property_name = match.groups()
            return self.find_objects_by_property(property_name, value)
        
        return []
    
    def _handle_count_query(self, query: str) -> int:
        """Handle count queries."""
        # Extract property and value from query
        # Pattern: "count objects where [property] is [value]"
        match = re.search(r'where\s+(\w+)\s+is\s+(\w+)', query)
        if match:
            property_name, value = match.groups()
            return self.count_by_property(property_name, value)
        
        # Pattern: "how many [value] [property]"
        match = re.search(r'how many\s+(\w+)\s+(\w+)', query)
        if match:
            value, property_name = match.groups()
            return self.count_by_property(property_name, value)
        
        # Pattern: "count all [property]"
        match = re.search(r'count all\s+(\w+)', query)
        if match:
            property_name = match.group(1)
            return len(self.objects)
        
        return 0
    
    def _handle_relation_query(self, query: str) -> List[Tuple[str, str, str]]:
        """Handle relation queries."""
        # Pattern: "find relations between [obj1] and [obj2]"
        match = re.search(r'between\s+(\w+)\s+and\s+(\w+)', query)
        if match:
            obj1, obj2 = match.groups()
            return self.find_relations_between(obj1, obj2)
        
        # Pattern: "find objects [relation] [obj]"
        match = re.search(r'(\w+)\s+(\w+)', query)
        if match:
            relation, obj = match.groups()
            return self.find_objects_with_relation(relation, obj)
        
        return []
    
    def _handle_compare_query(self, query: str) -> Dict[str, Any]:
        """Handle comparison queries."""
        # Pattern: "compare [obj1] and [obj2]"
        match = re.search(r'compare\s+(\w+)\s+and\s+(\w+)', query)
        if match:
            obj1, obj2 = match.groups()
            return self.compare_objects(obj1, obj2)
        
        return {}
    
    def _handle_general_query(self, query: str) -> Any:
        """Handle general queries that don't match specific patterns."""
        # Try to extract any property-value pair
        for property_name in ['shape', 'color', 'material', 'size']:
            if property_name in query:
                for value in self._get_all_values(property_name):
                    if value in query:
                        return self.find_objects_by_property(property_name, value)
        
        return []
    
    def find_objects_by_property(self, property_name: str, value: str) -> List[str]:
        """
        Find objects that have a specific property value.
        
        Args:
            property_name: Name of the property (shape, color, material, size)
            value: Value to search for
            
        Returns:
            List of object IDs that match the criteria
        """
        matching_objects = []
        property_name = property_name.lower()
        value = value.lower()
        
        for obj_id, properties in self.objects.items():
            if property_name in properties and properties[property_name].lower() == value:
                matching_objects.append(obj_id)
        
        return matching_objects
    
    def count_by_property(self, property_name: str, value: str) -> int:
        """
        Count objects that have a specific property value.
        
        Args:
            property_name: Name of the property (shape, color, material, size)
            value: Value to search for
            
        Returns:
            Number of objects that match the criteria
        """
        return len(self.find_objects_by_property(property_name, value))
    
    def find_relations_between(self, obj1: str, obj2: str) -> List[Tuple[str, str, str]]:
        """
        Find all relations between two objects.
        
        Args:
            obj1: First object ID
            obj2: Second object ID
            
        Returns:
            List of relation tuples (obj1, relation, obj2)
        """
        relations = []
        for rel_obj1, relation, rel_obj2 in self.relations:
            if (rel_obj1 == obj1 and rel_obj2 == obj2) or (rel_obj1 == obj2 and rel_obj2 == obj1):
                relations.append((rel_obj1, relation, rel_obj2))
        return relations
    
    def find_objects_with_relation(self, relation: str, target_obj: str) -> List[str]:
        """
        Find objects that have a specific relation to a target object.
        
        Args:
            relation: The relation type
            target_obj: The target object ID
            
        Returns:
            List of object IDs that have the relation to the target
        """
        related_objects = []
        for obj1, rel, obj2 in self.relations:
            if rel == relation:
                if obj1 == target_obj:
                    related_objects.append(obj2)
                elif obj2 == target_obj:
                    related_objects.append(obj1)
        return related_objects
    
    def compare_objects(self, obj1: str, obj2: str) -> Dict[str, Any]:
        """
        Compare two objects and return their similarities and differences.
        
        Args:
            obj1: First object ID
            obj2: Second object ID
            
        Returns:
            Dictionary with comparison results
        """
        if obj1 not in self.objects or obj2 not in self.objects:
            return {}
        
        props1 = self.objects[obj1]
        props2 = self.objects[obj2]
        
        similarities = []
        differences = []
        
        for prop in ['shape', 'color', 'material', 'size']:
            if props1[prop] == props2[prop]:
                similarities.append(f"{prop}: {props1[prop]}")
            else:
                differences.append(f"{prop}: {props1[prop]} vs {props2[prop]}")
        
        return {
            'similarities': similarities,
            'differences': differences,
            'obj1_properties': props1,
            'obj2_properties': props2
        }
    
    def _get_all_values(self, property_name: str) -> Set[str]:
        """
        Get all unique values for a given property.
        
        Args:
            property_name: Name of the property
            
        Returns:
            Set of all unique values for the property
        """
        values = set()
        for properties in self.objects.values():
            if property_name in properties:
                values.add(properties[property_name])
        return values
    
    def get_all_objects(self) -> List[str]:
        """Get all object IDs in the knowledge base."""
        return list(self.objects.keys())
    
    def get_object_properties(self, obj_id: str) -> Optional[Dict[str, str]]:
        """
        Get all properties of a specific object.
        
        Args:
            obj_id: Object ID to look up
            
        Returns:
            Dictionary of properties if object exists, None otherwise
        """
        return self.objects.get(obj_id)
    
    def get_all_relations(self) -> List[Tuple[str, str, str]]:
        """Get all relations in the knowledge base."""
        return self.relations.copy()
    
    def clear(self) -> None:
        """Clear all facts from the knowledge base."""
        self.facts.clear()
        self.objects.clear()
        self.relations.clear()
    
    def __len__(self) -> int:
        """Return the number of objects in the knowledge base."""
        return len(self.objects)
    
    def __str__(self) -> str:
        """String representation of the logic engine."""
        return f"SimpleLogicEngine({len(self.objects)} objects, {len(self.relations)} relations)"
    
    def __repr__(self) -> str:
        """Detailed string representation of the logic engine."""
        return f"SimpleLogicEngine(facts={len(self.facts)}, objects={list(self.objects.keys())})"
