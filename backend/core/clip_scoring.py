import pickle
from backend.core.embeddings.clip_model import get_clip_embedding
from backend.core.similarity.cosine import top_k_similarity
from backend.core.config import REFERENCE_EMBEDDINGS_PATH

with open(REFERENCE_EMBEDDINGS_PATH, "rb") as f:
    reference_embeddings = pickle.load(f)

def get_clip_score(image_path, category):
    if category not in reference_embeddings:
        raise ValueError(f"Invalid category: {category}")
    
    # 1. embedding of input image
    emb = get_clip_embedding(image_path)

    # 2. get reference embeddings
    refs = reference_embeddings[category]

    # 3. similarity
    score = top_k_similarity(emb, refs)

    return score