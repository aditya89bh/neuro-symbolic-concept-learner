from typing import List, Dict, Any
from src.scene.scene_graph import SceneGraph
from src.scene.objects import SceneObject
from .operations import filter_objects, query_attribute, count, exist


class SymbolicExecutor:
    def __init__(self, scene: SceneGraph):
        self.scene = scene

    def execute(self, program: List[Dict[str, Any]]):
        current_objects: List[SceneObject] = self.scene.get_all_objects()
        trace = []

        for step in program:
            op = step.get("op")

            if op == "filter":
                attribute = step["attribute"]
                value = step["value"]
                current_objects = filter_objects(current_objects, attribute, value)
                trace.append(f"Filtered objects where {attribute}={value}")

            elif op == "relate":
                relation = step["relation"]
                if not current_objects:
                    return None, trace

                reference_obj = current_objects[0]

                if relation == "left_of":
                    current_objects = self.scene.left_of(reference_obj)
                elif relation == "right_of":
                    current_objects = self.scene.right_of(reference_obj)
                elif relation == "above":
                    current_objects = self.scene.above(reference_obj)
                elif relation == "below":
                    current_objects = self.scene.below(reference_obj)

                trace.append(f"Applied relation {relation} on {reference_obj.id}")

            elif op == "query":
                attribute = step["attribute"]
                if not current_objects:
                    return None, trace

                result = query_attribute(current_objects[0], attribute)
                trace.append(f"Queried attribute {attribute}")
                return result, trace

            elif op == "count":
                result = count(current_objects)
                trace.append("Counted objects")
                return result, trace

            elif op == "exist":
                result = exist(current_objects)
                trace.append("Checked existence")
                return result, trace

        return current_objects, trace
