from fastapi import APIRouter, Query
from app.services.faiss_store_db import search_index
from app.services.embedding_model import embedding_single
from app.config import settings
import numpy as np

router = APIRouter(prefix="/retrieve", tags=["retrieve"])

@router.get("")
async def retrieve(query: str = Query(...), top_k: int = Query(3, le=10)):
    if not query.strip():
        return {"results": []}
    
    query_embedding = np.array([embedding_single(query)], dtype=np.float32)
    results = search_index(query_embedding, top_k=top_k)
    
    return {
        "results": [
            {"text": t, "similarity_score": round(float(s), 4)} for t, s in results
        ]
    }
    
    
    