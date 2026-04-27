from abc import ABC, abstractmethod
from typing import Any, List


class ConceptLearner(ABC):
    """Abstract interface for learning and grounding visual concepts."""

    @abstractmethod
    def extract_concepts(self, features: Any) -> List[str]:
        """Return concept labels present in the given feature representation."""

    @abstractmethod
    def ground_concept(self, concept: str, features: Any) -> float:
        """Return a confidence score [0, 1] that a concept applies to features."""

    @abstractmethod
    def learn_concept(
        self,
        name: str,
        positive_examples: List[Any],
        negative_examples: List[Any],
    ) -> None:
        """Update concept representations from labelled examples."""
