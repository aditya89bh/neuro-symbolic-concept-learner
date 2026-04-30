from dataclasses import dataclass


@dataclass
class SceneObject:
    id: str
    shape: str
    color: str
    size: str
    x: float
    y: float
