import torch
import clip
from backend.core.utils.image_loader import load_image

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load("ViT-B/32", device=device)

def get_clip_embedding(image_path):
    image = preprocess(load_image(image_path)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        embedding = model.encode_image(image)
    
    return embedding.cpu().numpy().flatten()