from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)

text_chunks = []

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk.strip()) > 30:
            chunks.append(chunk)
    return chunks


def build_vector_store(chunks: list[str]):
    global index, text_chunks
    index.reset()
    text_chunks.clear()

    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    index.add(embeddings)
    text_chunks.extend(chunks)

def query_top_k(question: str, k: int =3):
    q_embedding = embedder.encode([question])
    D, I = index.search(np.array(q_embedding), k)
    results = [text_chunks[i] for i in I[0]]
    return results

