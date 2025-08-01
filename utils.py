import os
import shutil
import nltk
from nltk.tokenize import sent_tokenize

# 🚨 Force delete broken punkt if it exists
corrupted_path = os.path.join(nltk.data.find('tokenizers').path, 'punkt')
if os.path.exists(corrupted_path):
    shutil.rmtree(corrupted_path, ignore_errors=True)

# ✅ Now ensure clean download
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


def load_articles(directory):
    """
    Loads and chunks all .txt articles in the given directory.
    Returns: List of tuples (chunk_text, source_filename)
    """
    all_chunks = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                text = f.read()
                chunks = chunk_text(text)
                all_chunks.extend([(chunk, filename) for chunk in chunks])
    return all_chunks


def chunk_text(text, max_tokens=100):
    """
    Splits long text into smaller chunks of approx. max_tokens size.
    """
    sentences = sent_tokenize(text)
    chunks, current_chunk, current_length = [], [], 0

    for sentence in sentences:
        tokens = sentence.split()
        if current_length + len(tokens) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = tokens
            current_length = len(tokens)
        else:
            current_chunk.extend(tokens)
            current_length += len(tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
