from sentence_transformers import SentenceTransformer
import chromadb
from utils import load_articles
import os

# ✅ Setup persistent ChromaDB client
client = chromadb.Client()
collection = client.get_or_create_collection(name="help_articles")

# ✅ Load sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


def build_vector_db():
    """
    Builds the ChromaDB vector store from articles.
    Each chunk is embedded and stored with its source filename as metadata.
    """
    chunks_with_sources = load_articles("articles")  # [(chunk, source), ...]
    texts = [chunk for chunk, _ in chunks_with_sources]
    sources = [source for _, source in chunks_with_sources]
    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(texts))],
        metadatas=[{"source": source} for source in sources]  # Ensure each is a dict!
    )

    print(f"✅ Loaded {len(texts)} chunks into ChromaDB.")


def retrieve_context(query, k=3, return_sources=False):
    """
    Retrieves top-k relevant chunks using semantic search.
    Optionally returns associated source filenames.
    """
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )

    chunks = results["documents"][0]
    sources = []

    if return_sources:
        metadatas = results.get("metadatas", [[]])[0]
        for meta in metadatas:
            if isinstance(meta, dict):
                source_path = meta.get("source", "Unknown")
            else:
                source_path = "Unknown"
            filename = os.path.basename(source_path) if source_path else "Unknown"
            sources.append(filename)
        return chunks, sources

    return chunks
