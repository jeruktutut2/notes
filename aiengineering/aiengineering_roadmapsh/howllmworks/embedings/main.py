from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Kucing tidur di sofa",
    "Anjing bermain di taman",
    "Mobil balap merah"
]

embeddings = model.encode(sentences)
print(embeddings)

# Hitung kemiripan antar kalimat
from sklearn.metrics.pairwise import cosine_similarity

sim = cosine_similarity(embeddings)
print(sim)
# Kucing vs Anjing: ~0.65 (mirip — sama-sama hewan)
# Kucing vs Mobil: ~0.12 (jauh)