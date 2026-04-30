from typing import List
from src.scene.objects import SceneObject


def filter_objects(objects: List[SceneObject], attribute: str, value: str) -> List[SceneObject]:
    return [obj for obj in objects if getattr(obj, attribute) == value]


def query_attribute(obj: SceneObject, attribute: str):
    return getattr(obj, attribute)


def count(objects: List[SceneObject]) -> int:
    return len(objects)


def exist(objects: List[SceneObject]) -> bool:
    return len(objects) > 0
