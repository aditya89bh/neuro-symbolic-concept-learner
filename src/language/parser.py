import re
from typing import Dict, List, Optional


class QuestionParser:
    COLORS = {"red", "blue", "green", "yellow", "black", "white"}
    SHAPES = {"cube", "sphere", "cylinder", "cone"}
    SIZES = {"small", "large", "medium", "tiny", "big"}
    RELATIONS = {
        "left of": "left_of",
        "right of": "right_of",
        "above": "above",
        "below": "below",
    }

    def parse(self, question: str) -> Optional[List[Dict[str, str]]]:
        normalized = question.lower().strip().rstrip("?")

        attribute_query = self._parse_attribute_query(normalized)
        if attribute_query:
            return attribute_query

        relation_query = self._parse_relation_query(normalized)
        if relation_query:
            return relation_query

        count_query = self._parse_count_query(normalized)
        if count_query:
            return count_query

        exist_query = self._parse_exist_query(normalized)
        if exist_query:
            return exist_query

        return None

    def _parse_attribute_query(self, question: str):
        match = re.match(r"what (color|size) is the (.+)", question)
        if not match:
            return None

        target_attribute, description = match.groups()
        program = self._description_to_filters(description)
        program.append({"op": "query", "attribute": target_attribute})
        return program

    def _parse_relation_query(self, question: str):
        for phrase, relation in self.RELATIONS.items():
            match = re.match(rf"what(?: color)? is (?:the object )?{phrase} the (.+)", question)
            if match:
                description = match.group(1)
                program = self._description_to_filters(description)
                program.append({"op": "relate", "relation": relation})
                program.append({"op": "query", "attribute": "color"})
                return program
        return None

    def _parse_count_query(self, question: str):
        match = re.match(r"how many (.+) objects are there", question)
        if not match:
            return None

        description = match.group(1)
        program = self._description_to_filters(description)
        program.append({"op": "count"})
        return program

    def _parse_exist_query(self, question: str):
        match = re.match(r"is there an? (.+)", question)
        if not match:
            return None

        description = match.group(1)
        program = self._description_to_filters(description)
        program.append({"op": "exist"})
        return program

    def _description_to_filters(self, description: str):
        tokens = description.split()
        program = []

        for token in tokens:
            if token in self.COLORS:
                program.append({"op": "filter", "attribute": "color", "value": token})
            elif token in self.SHAPES:
                program.append({"op": "filter", "attribute": "shape", "value": token})
            elif token in self.SIZES:
                normalized_size = "large" if token in {"big"} else token
                program.append({"op": "filter", "attribute": "size", "value": normalized_size})

        return program
