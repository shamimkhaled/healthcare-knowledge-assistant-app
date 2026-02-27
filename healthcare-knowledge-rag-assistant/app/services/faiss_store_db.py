import faiss
import numpy as np
import pickle
from pathlib import Path


INDEX_PATH = Path("faiss_index")
METADATA_PATH = INDEX_PATH / "metadata.pkl"


def _ensure_index_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        
def get_faiss_index():
    _ensure_index_dir(INDEX_PATH)
    index_file = INDEX_PATH / "index.faiss"
    
    if index_file.exists():
        return faiss.read_index(str(index_file))
    else:
        # Create a new index (using L2 distance)
        
        dim = 384 # Assume 384 dimensional embeddings
        index = faiss.IndexFlatL2(dim)  
        return index
    
    
def get_metadata():
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)
    else:
        return []
    

def save_faiss_index(index: faiss.Index, metadata: list):
    _ensure_index_dir(INDEX_PATH)
    index_file = INDEX_PATH / "index.faiss"
    faiss.write_index(index, str(index_file))
    
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
        
def add_to_index(embeddings: np.ndarray, metadata_entries: list):
    index = get_faiss_index()
    metadata = get_metadata()
    
    index.add(embeddings.astype(np.float32))
    metadata.extend(metadata_entries)
    
    save_faiss_index(index, metadata)
    
def search_index(query_embedding: np.ndarray, top_k: int = 3) -> list[tuple[str, float]]:
    index = get_faiss_index()
    metadata = get_metadata()
    
    if index.ntotal == 0:
        return []
    
    # Over-fetch to improve unique result count
    total = index.ntotal
    fetch_k = min(total, max(top_k * 5, top_k))
    distances, indices = index.search(query_embedding.astype(np.float32), fetch_k)

    results = []
    seen_indices = set()
    seen_texts = set()
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(metadata) or idx in seen_indices:
            continue
        text = metadata[idx]["text"]
        if text in seen_texts:
            continue
        seen_indices.add(idx)
        seen_texts.add(text)
        similarity = 1 / (1 + float(dist))  # Convert distance to similarity
        results.append((text, similarity))
        if len(results) >= top_k:
            break

    # If still not enough, fetch all and try again
    if len(results) < top_k and fetch_k < total:
        distances, indices = index.search(query_embedding.astype(np.float32), total)
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(metadata) or idx in seen_indices:
                continue
            text = metadata[idx]["text"]
            if text in seen_texts:
                continue
            seen_indices.add(idx)
            seen_texts.add(text)
            similarity = 1 / (1 + float(dist))
            results.append((text, similarity))
            if len(results) >= top_k:
                break

    return results