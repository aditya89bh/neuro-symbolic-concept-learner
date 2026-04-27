"""
Concepts Module - Concept Learning and Representation

This module handles concept learning and representation including:
- Concept extraction from visual and textual data
- Concept hierarchy construction
- Concept grounding in visual features
- Abstract concept formation
- Concept similarity and relationship learning
- Concept-based feature aggregation

The module learns both concrete visual concepts (objects, attributes)
and abstract concepts (spatial relations, actions) that can be
used for symbolic reasoning.
"""

from src.concepts.concept_learner import ConceptLearner

__all__ = ["ConceptLearner"]
