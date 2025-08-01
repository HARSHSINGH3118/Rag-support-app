from sentence_transformers import SentenceTransformer
import chromadb
from utils import load_articles

# ✅ Setup persistent ChromaDB client
client = chromadb.PersistentClient(path="./db")
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

def retrieve_context(query: str, k=3, return_sources=False):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k, include=["documents", "metadatas"])

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if return_sources:
        # 🔐 Protect against None metadata
        sources = [(meta.get("source") if isinstance(meta, dict) else "Unknown") for meta in metadatas]
        return documents, sources
    else:
        return documents
