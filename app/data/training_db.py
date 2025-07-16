# training_db.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

TRAINING_DATABASE = {
    "Python": {
        1: {"course_id": "PY101", "name": "Python Fundamentals", "embedding": np.random.rand(300)},
        2: {"course_id": "PY201", "name": "Python Data Analysis", "embedding": np.random.rand(300)}
    }
}

def find_similar_courses(query: str, top_n: int = 3):
    """Fallback when exact skill not found"""
    query_vec = np.random.rand(300)  # Replace with actual embedding
    similarities = []
    
    for skill in TRAINING_DATABASE.values():
        for course in skill.values():
            sim = cosine_similarity(
                [query_vec],
                [course["embedding"]]
            )[0][0]
            similarities.append((sim, course))
            
    return [course for (sim, course) in sorted(similarities, reverse=True)[:top_n]]