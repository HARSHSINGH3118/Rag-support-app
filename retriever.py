from sentence_transformers import SentenceTransformer
import chromadb
from utils import load_articles

# ✅ Setup ChromaDB correctly
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="help_articles")

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_vector_db():
    chunks = load_articles("articles")
    embeddings = model.encode(chunks).tolist()
    collection.add(documents=chunks, embeddings=embeddings, ids=[f"doc_{i}" for i in range(len(chunks))])
    print(f"✅ Loaded {len(chunks)} chunks into ChromaDB.")

def retrieve_context(query: str, k=3):
    query_embedding = model.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]
