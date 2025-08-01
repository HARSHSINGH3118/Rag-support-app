import os
from nltk.tokenize import sent_tokenize
import nltk

nltk.data.path.append("C:/Users/harsh/AppData/Roaming/nltk_data")



def load_articles(directory):
    all_chunks = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                text = f.read()
                chunks = chunk_text(text)
                all_chunks.extend(chunks)
    return all_chunks

def chunk_text(text, max_tokens=100):
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
