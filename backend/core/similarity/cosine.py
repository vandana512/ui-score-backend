import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def compute_cosine(vec1, vec2):
    return cosine_similarity([vec1], [vec2])[0][0]

def top_k_similarity(test_vec, reference_vecs, k=3):
    sims = [compute_cosine(test_vec, ref) for ref in reference_vecs]
    sims.sort(reverse=True)
    return np.mean(sims[:k])