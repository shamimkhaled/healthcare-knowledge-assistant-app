from fastapi import APIRouter, Depends, Query
from app.services.faiss_store_db import search_index, get_metadata
from app.services.embedding_model import embedding_texts, get_embedding_model, embedding_single
from app.config import settings
import numpy as np

router = APIRouter(prefix="/retrieve", tags=["retrieve"])

@router.get("")
async def retrieve(query: str = Query(...), top_k: int = Query(3, le=10)):
    if not query.strip():
        return {"results": []}
    
    embedding_model = get_embedding_model(settings.EMBEDDING_MODEL)
    query_embedding = np.array([embedding_single(query)], dtype=np.float32)
    results = search_index(query_embedding, top_k=top_k)
    
    return {
        
        "results": [{"text": t, "similarity_score": round(s, 4)} for t, s in results]
    }
    
    
    