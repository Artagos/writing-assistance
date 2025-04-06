class TextPart:
    def __init__(self, id, type, content_goal):
        self.id = id
        self.type = type  # 'Introduction', 'Paragraph', 'Enumeration', etc.
        self.content_goal = content_goal  # What this part wants to say

    def __repr__(self):
        return f"{self.type}(id={self.id}, content_goal={self.content_goal[:40]}...)"

class Relation:
    def __init__(self, from_id, to_id, relation_type):
        self.from_id = from_id
        self.to_id = to_id
        self.relation_type = relation_type  # 'precedes', 'is part of', etc.

    def __repr__(self):
        return f"{self.relation_type}({self.from_id} -> {self.to_id})"

import spacy
import uuid

nlp = spacy.load("en_core_web_sm")

def extract_parts_and_relations(description: str):
    doc = nlp(description)
    parts = []
    relations = []

    current_id = lambda: str(uuid.uuid4())
    last_part_id = None

    for sent in doc.sents:
        text = sent.text.strip()
        lower = text.lower()

        if "introduction" in lower:
            part_type = "Introduction"
        elif "paragraph" in lower:
            part_type = "Paragraph"
        elif "enumeration" in lower or "list" in lower or "bullet" in lower:
            part_type = "Enumeration"
        else:
            part_type = "Other"

        part_id = current_id()
        part = TextPart(id=part_id, type=part_type, content_goal=text)
        parts.append(part)

        if last_part_id:
            relations.append(Relation(from_id=last_part_id, to_id=part_id, relation_type="precedes"))

        last_part_id = part_id

    return parts, relations


description = """
El texto comienza con una introducción que presenta el tema y su importancia.
Luego, hay dos párrafos que elaboran el argumento central con ejemplos.
Después, una lista con viñetas resume los puntos principales.
Finalmente, una conclusión refuerza el mensaje.
"""

parts, relations = extract_parts_and_relations(description)

for p in parts:
    print(p)

print("\nRelations:")
for r in relations:
    print(r)
