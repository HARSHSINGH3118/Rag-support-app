import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_articles
from typing import List, Tuple, Optional

# Global storage for chunks, sources, and embeddings
chunks: List[str] = []
sources: List[str] = []
embeddings: Optional[np.ndarray] = None

# Load sentence embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def build_vector_db():
    """
    Builds an in-memory vector store from article chunks.
    Each chunk is embedded and stored with its source filename.
    """
    global chunks, sources, embeddings

    # Always resolve articles directory relative to this file
    base_dir = os.path.dirname(__file__)
    articles_dir = os.path.join(base_dir, "articles")

    data: List[Tuple[str, str]] = load_articles(articles_dir)
    if not data:
        print(f"⚠️ No articles/chunks found in '{articles_dir}'.")
        embeddings = None
        return

    # Unzip into parallel lists
    chunks_list, sources_list = zip(*data)
    chunks = list(chunks_list)
    sources = list(sources_list)

    # Compute embeddings matrix
    embeddings = model.encode(chunks, convert_to_numpy=True)
    print(f"✅ Loaded {len(chunks)} chunks into in-memory DB.")

def retrieve_context(query: str, k: int = 3, return_sources: bool = False):
    """
    Retrieves top-k relevant chunks for a query based on cosine similarity.
    If return_sources=True, also returns the source filenames.
    """
    global embeddings, chunks, sources

    # Lazy-build if needed
    if embeddings is None:
        build_vector_db()
        if embeddings is None:
            return ([], []) if return_sources else []

    # Embed the query and compute similarities
    q_emb = model.encode([query], convert_to_numpy=True)
    scores = cosine_similarity(q_emb, embeddings)[0]

    # Get top-k indices
    idxs = np.argsort(scores)[::-1][:k]
    selected_chunks = [chunks[i] for i in idxs]

    if return_sources:
        selected_sources = [sources[i] for i in idxs]
        return selected_chunks, selected_sources

    return selected_chunks
