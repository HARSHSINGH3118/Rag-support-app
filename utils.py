import os
import re
import nltk

# Try to load punkt; if it fails, we’ll fallback later
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass  # if download fails (e.g. offline), we’ll fallback

from nltk.tokenize import sent_tokenize

def load_articles(directory):
    """
    Loads and chunks all .txt articles in the given directory.
    Returns: List of tuples (chunk_text, source_filename)
    """
    all_chunks = []
    directory = os.path.abspath(directory)

    if not os.path.isdir(directory):
        print(f"⚠️ Directory not found: {directory}")
        return all_chunks

    found = False
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith(".txt"):
            continue
        found = True
        path = os.path.join(directory, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if not text:
                continue
            for chunk in chunk_text(text):
                all_chunks.append((chunk, fname))
        except Exception as e:
            print(f"⚠️ Failed to process {fname}:\n{e}")

    if not found:
        print(f"⚠️ No articles found in '{directory}' folder.")
    return all_chunks

def chunk_text(text: str, max_tokens: int = 100) -> list[str]:
    """
    Splits text into chunks of at most max_tokens words.
    Falls back to regex sentence splitting if punkt is unavailable.
    """
    # 1) Try NLTK sentence tokenizer
    try:
        sentences = sent_tokenize(text)
    except (LookupError, Exception):
        # Fallback: split on ., !, ? followed by whitespace
        sentences = re.split(r'(?<=[\.\!\?])\s+', text)

    chunks = []
    current, length = [], 0

    for sent in sentences:
        words = sent.split()
        if length + len(words) > max_tokens:
            if current:
                chunks.append(" ".join(current))
            current = words
            length = len(words)
        else:
            current.extend(words)
            length += len(words)

    if current:
        chunks.append(" ".join(current))

    return chunks
