import json
from typing import List
from .objects import SceneObject


class SceneGraph:
    def __init__(self, objects: List[SceneObject]):
        self.objects = objects

    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as f:
            data = json.load(f)

        objects = [
            SceneObject(**obj)
            for obj in data.get("objects", [])
        ]

        return cls(objects)

    def get_all_objects(self) -> List[SceneObject]:
        return self.objects

    def filter(self, attribute: str, value: str) -> List[SceneObject]:
        return [obj for obj in self.objects if getattr(obj, attribute) == value]

    def left_of(self, reference_obj: SceneObject) -> List[SceneObject]:
        return [obj for obj in self.objects if obj.x < reference_obj.x]

    def right_of(self, reference_obj: SceneObject) -> List[SceneObject]:
        return [obj for obj in self.objects if obj.x > reference_obj.x]

    def above(self, reference_obj: SceneObject) -> List[SceneObject]:
        return [obj for obj in self.objects if obj.y > reference_obj.y]

    def below(self, reference_obj: SceneObject) -> List[SceneObject]:
        return [obj for obj in self.objects if obj.y < reference_obj.y]
