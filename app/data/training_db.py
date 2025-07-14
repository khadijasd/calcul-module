from typing import Dict
import numpy as np
from .skill_embeddings import get_skill_vector  # See file below

TRAINING_DATABASE = {
    "Python": {
        1: {
            "course_id": "PY101",
            "name": "Python Fundamentals",
            "description": "Intro to Python syntax and basic programming",
            "embedding": get_skill_vector("Python Fundamentals"),  # Pre-computed
            "popularity": 0.92
        },
        # ... other levels
    },
    # ... other skills
}

SKILL_ALIASES = {
    "PY": "Python",
    "ML": "Machine Learning"
}

def find_similar_courses(query: str, top_n: int = 3) -> list:
    """Fallback when exact skill not found"""
    query_embedding = get_skill_vector(query)
    similarities = []
    for skill in TRAINING_DATABASE.values():
        for course in skill.values():
            sim = cosine_similarity(
                [query_embedding], 
                [course["embedding"]]
            )[0][0]
            similarities.append((sim, course))
    return sorted(similarities, reverse=True)[:top_n]