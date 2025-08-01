from sentence_transformers import SentenceTransformer
import chromadb
from utils import load_articles
import os

# ✅ Use in-memory Chroma client for Streamlit Cloud
client = chromadb.EphemeralClient()
collection = client.get_or_create_collection(name="help_articles")

# ✅ Load sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def build_vector_db():
    chunks_with_sources = load_articles("articles")  # [(chunk, source), ...]
    texts = [chunk for chunk, _ in chunks_with_sources]
    sources = [source for _, source in chunks_with_sources]
    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(texts))],
        metadatas=[{"source": source} for source in sources]
    )

    print(f"✅ Loaded {len(texts)} chunks into ChromaDB.")

def retrieve_context(query, k=3, return_sources=False):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )

    chunks = results["documents"][0]
    sources = [os.path.basename(m.get("source", "Unknown")) for m in results["metadatas"][0]]

    return (chunks, sources) if return_sources else chunks
