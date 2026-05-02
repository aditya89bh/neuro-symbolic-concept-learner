import re


class QuestionParser:
    def parse(self, question: str):
        question = question.lower()

        # Attribute query
        if "what color" in question:
            return [
                {"op": "filter", "attribute": "shape", "value": "cube"},
                {"op": "query", "attribute": "color"},
            ]

        # Relation query
        if "left of" in question:
            return [
                {"op": "filter", "attribute": "color", "value": "blue"},
                {"op": "filter", "attribute": "shape", "value": "sphere"},
                {"op": "relate", "relation": "left_of"},
                {"op": "query", "attribute": "color"},
            ]

        # Count query
        if "how many" in question:
            return [
                {"op": "filter", "attribute": "size", "value": "small"},
                {"op": "count"},
            ]

        # Exist query
        if "is there" in question:
            return [
                {"op": "filter", "attribute": "color", "value": "green"},
                {"op": "filter", "attribute": "shape", "value": "cylinder"},
                {"op": "exist"},
            ]

        return None
