from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VisualProcessor(ABC):
    """Abstract interface for visual scene processing."""

    @abstractmethod
    def process(self, image_path: str) -> Dict[str, Any]:
        """Process an image and return a full scene description."""

    @abstractmethod
    def detect_objects(self, image_path: str) -> List[Dict[str, Any]]:
        """Detect and segment individual objects in an image."""

    @abstractmethod
    def extract_features(self, image_path: str) -> Any:
        """Extract feature representations from an image."""

    @abstractmethod
    def detect_relations(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Infer spatial relations between a list of detected objects."""
