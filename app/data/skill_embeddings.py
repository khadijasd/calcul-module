# Updated skill_embeddings.py
import spacy
from sklearn.metrics.pairwise import cosine_similarity

# Load small English model (12MB)
nlp = spacy.load("en_core_web_sm") 

def get_skill_vector(skill_name: str):
    return nlp(skill_name.lower()).vector

def skill_similarity(skill1: str, skill2: str) -> float:
    v1 = get_skill_vector(skill1)
    v2 = get_skill_vector(skill2)
    return cosine_similarity([v1], [v2])[0][0]