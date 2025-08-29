"""
Scene Graph Representation for CLEVR Dataset

This module provides a SceneGraph class that represents visual scenes as
structured graphs with objects and their spatial relationships. It's designed
specifically for the CLEVR dataset and supports conversion to logic programming
predicates for symbolic reasoning.
"""

from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass
from enum import Enum
import math


class Shape(Enum):
    """Valid shapes in CLEVR dataset."""
    CUBE = "cube"
    SPHERE = "sphere"
    CYLINDER = "cylinder"


class Color(Enum):
    """Valid colors in CLEVR dataset."""
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PURPLE = "purple"
    CYAN = "cyan"
    BROWN = "brown"
    GRAY = "gray"


class Material(Enum):
    """Valid materials in CLEVR dataset."""
    METAL = "metal"
    RUBBER = "rubber"


class Size(Enum):
    """Valid sizes in CLEVR dataset."""
    SMALL = "small"
    LARGE = "large"


class SpatialRelation(Enum):
    """Valid spatial relations between objects."""
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    BEHIND = "behind"
    FRONT_OF = "front_of"
    ABOVE = "above"
    BELOW = "below"
    SAME_X = "same_x"
    SAME_Y = "same_y"
    SAME_Z = "same_z"


@dataclass
class Position:
    """3D position of an object in the scene."""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Position') -> float:
        """Calculate Euclidean distance to another position."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)


@dataclass
class Object:
    """Represents an object in the scene with all its properties."""
    obj_id: str
    shape: Shape
    color: Color
    material: Material
    size: Size
    position: Position
    
    def __post_init__(self):
        """Validate object properties after initialization."""
        if not isinstance(self.shape, Shape):
            raise ValueError(f"shape must be a Shape enum, got {type(self.shape)}")
        if not isinstance(self.color, Color):
            raise ValueError(f"color must be a Color enum, got {type(self.color)}")
        if not isinstance(self.material, Material):
            raise ValueError(f"material must be a Material enum, got {type(self.material)}")
        if not isinstance(self.size, Size):
            raise ValueError(f"size must be a Size enum, got {type(self.size)}")
        if not isinstance(self.position, Position):
            raise ValueError(f"position must be a Position object, got {type(self.position)}")


class SceneGraph:
    """
    A graph representation of a visual scene with objects and spatial relationships.
    
    This class stores objects with their properties (shape, color, material, size, position)
    and spatial relationships between objects. It supports conversion to logic programming
    predicates for symbolic reasoning tasks.
    
    Attributes:
        objects: Dictionary mapping object IDs to Object instances
        relations: Dictionary mapping (obj1_id, relation, obj2_id) tuples to boolean values
        next_obj_id: Counter for generating unique object IDs
    """
    
    def __init__(self):
        """Initialize an empty scene graph."""
        self.objects: Dict[str, Object] = {}
        self.relations: Dict[Tuple[str, SpatialRelation, str], bool] = {}
        self._next_obj_id = 1
    
    def add_object(
        self,
        shape: Shape,
        color: Color,
        material: Material,
        size: Size,
        position: Position,
        obj_id: Optional[str] = None
    ) -> str:
        """
        Add an object to the scene graph.
        
        Args:
            shape: The shape of the object (cube, sphere, cylinder)
            color: The color of the object
            material: The material of the object (metal, rubber)
            size: The size of the object (small, large)
            position: The 3D position of the object
            obj_id: Optional custom object ID. If None, generates automatic ID
            
        Returns:
            The object ID of the added object
            
        Raises:
            ValueError: If obj_id already exists or invalid properties provided
        """
        if obj_id is None:
            obj_id = f"obj{self._next_obj_id}"
            self._next_obj_id += 1
        
        if obj_id in self.objects:
            raise ValueError(f"Object with ID '{obj_id}' already exists")
        
        obj = Object(obj_id, shape, color, material, size, position)
        self.objects[obj_id] = obj
        return obj_id
    
    def add_relation(
        self,
        obj1_id: str,
        relation: SpatialRelation,
        obj2_id: str,
        value: bool = True
    ) -> None:
        """
        Add a spatial relation between two objects.
        
        Args:
            obj1_id: ID of the first object
            relation: The spatial relation type
            obj2_id: ID of the second object
            value: Boolean value indicating if the relation holds (default: True)
            
        Raises:
            ValueError: If either object doesn't exist
        """
        if obj1_id not in self.objects:
            raise ValueError(f"Object '{obj1_id}' not found in scene")
        if obj2_id not in self.objects:
            raise ValueError(f"Object '{obj2_id}' not found in scene")
        
        self.relations[(obj1_id, relation, obj2_id)] = value
    
    def get_object(self, obj_id: str) -> Optional[Object]:
        """
        Get an object by its ID.
        
        Args:
            obj_id: The object ID to look up
            
        Returns:
            The Object instance if found, None otherwise
        """
        return self.objects.get(obj_id)
    
    def get_objects_by_property(
        self,
        shape: Optional[Shape] = None,
        color: Optional[Color] = None,
        material: Optional[Material] = None,
        size: Optional[Size] = None
    ) -> List[Object]:
        """
        Get objects that match the specified properties.
        
        Args:
            shape: Filter by shape (optional)
            color: Filter by color (optional)
            material: Filter by material (optional)
            size: Filter by size (optional)
            
        Returns:
            List of objects matching the specified properties
        """
        matching_objects = []
        
        for obj in self.objects.values():
            if shape is not None and obj.shape != shape:
                continue
            if color is not None and obj.color != color:
                continue
            if material is not None and obj.material != material:
                continue
            if size is not None and obj.size != size:
                continue
            matching_objects.append(obj)
        
        return matching_objects
    
    def get_relations(self, obj_id: str) -> List[Tuple[SpatialRelation, str, bool]]:
        """
        Get all relations involving a specific object.
        
        Args:
            obj_id: The object ID to get relations for
            
        Returns:
            List of tuples (relation, other_obj_id, value)
        """
        relations = []
        for (obj1, relation, obj2), value in self.relations.items():
            if obj1 == obj_id:
                relations.append((relation, obj2, value))
            elif obj2 == obj_id:
                # For symmetric relations, we might want to include both directions
                relations.append((relation, obj1, value))
        return relations
    
    def to_predicates(self) -> List[str]:
        """
        Convert the scene graph to logic programming predicates.
        
        Returns:
            List of predicate strings in the format:
            - "Object(obj_id, shape, color, material, size)" for objects
            - "Relation(obj1_id, relation, obj2_id)" for relations
        """
        predicates = []
        
        # Add object predicates
        for obj in self.objects.values():
            predicate = f"Object({obj.obj_id}, {obj.shape.value}, {obj.color.value}, {obj.material.value}, {obj.size.value})"
            predicates.append(predicate)
        
        # Add relation predicates
        for (obj1_id, relation, obj2_id), value in self.relations.items():
            if value:  # Only include relations that are True
                predicate = f"Relation({obj1_id}, {relation.value}, {obj2_id})"
                predicates.append(predicate)
        
        return predicates
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the scene graph to a dictionary representation.
        
        Returns:
            Dictionary representation of the scene graph
        """
        objects_dict = {}
        for obj_id, obj in self.objects.items():
            objects_dict[obj_id] = {
                'shape': obj.shape.value,
                'color': obj.color.value,
                'material': obj.material.value,
                'size': obj.size.value,
                'position': {
                    'x': obj.position.x,
                    'y': obj.position.y,
                    'z': obj.position.z
                }
            }
        
        relations_list = []
        for (obj1_id, relation, obj2_id), value in self.relations.items():
            if value:
                relations_list.append({
                    'obj1': obj1_id,
                    'relation': relation.value,
                    'obj2': obj2_id
                })
        
        return {
            'objects': objects_dict,
            'relations': relations_list
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SceneGraph':
        """
        Create a SceneGraph from a dictionary representation.
        
        Args:
            data: Dictionary with 'objects' and 'relations' keys
            
        Returns:
            New SceneGraph instance
        """
        scene = cls()
        
        # Add objects
        for obj_id, obj_data in data['objects'].items():
            position = Position(
                obj_data['position']['x'],
                obj_data['position']['y'],
                obj_data['position']['z']
            )
            scene.add_object(
                shape=Shape(obj_data['shape']),
                color=Color(obj_data['color']),
                material=Material(obj_data['material']),
                size=Size(obj_data['size']),
                position=position,
                obj_id=obj_id
            )
        
        # Add relations
        for rel_data in data['relations']:
            scene.add_relation(
                obj1_id=rel_data['obj1'],
                relation=SpatialRelation(rel_data['relation']),
                obj2_id=rel_data['obj2']
            )
        
        return scene
    
    def __len__(self) -> int:
        """Return the number of objects in the scene."""
        return len(self.objects)
    
    def __contains__(self, obj_id: str) -> bool:
        """Check if an object exists in the scene."""
        return obj_id in self.objects
    
    def __str__(self) -> str:
        """String representation of the scene graph."""
        obj_count = len(self.objects)
        rel_count = sum(1 for v in self.relations.values() if v)
        return f"SceneGraph({obj_count} objects, {rel_count} relations)"
    
    def __repr__(self) -> str:
        """Detailed string representation of the scene graph."""
        return f"SceneGraph(objects={list(self.objects.keys())}, relations={list(self.relations.keys())})"
