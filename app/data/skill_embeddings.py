import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# New skill_embeddings.py
def load_model():
    for path in [
        '/root/.cache/fasttext/cc.en.300.bin',
        os.path.expanduser('~/.cache/fasttext/cc.en.300.bin'),
        './cc.en.300.bin'
    ]:
        if os.path.exists(path):
            return fasttext.load_model(path)
    raise FileNotFoundError("Model missing")

EMBEDDING_MODEL = load_model()  # Tries multiple locations

def get_skill_vector(skill_name: str) -> np.array:
    """Convert skill name to 300D vector"""
    return EMBEDDING_MODEL.get_sentence_vector(skill_name.lower())

def skill_similarity(skill1: str, skill2: str) -> float:
    """Compare two skills semantically"""
    v1 = get_skill_vector(skill1)
    v2 = get_skill_vector(skill2)
    return cosine_similarity([v1], [v2])[0][0]