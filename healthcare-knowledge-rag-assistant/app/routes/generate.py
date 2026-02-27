from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from app.srvices.embedding_model import embedding_single, get_embedding_model
from app.services.faiss_store_db import search_index
from app.config import settings
import numpy as np
from app.services.translate import translate_text

router = APIRouter(prefix="/generate", tags=["generate"])

class GenerateRequest(BaseModel):
    query: str
    target_language: Optional[str] = None
    
@router.post("")
async def generate_response(request: GenerateRequest):
    embeddin_model = get_embedding_model(settings.EMBEDDING_MODEL)
    query_embedding = np.array([embedding_single(request.query)], dtype=np.float32)
    results = search_index(query_embedding, top_k=3)
    
    
    context = "\n\n".join([t for t, _ in results]) if results else "No relevant documents found."
    
    
    response = f"Based on the retrieved context, here is a response to your query:\n\n{context}"
    
    if request.target_language:
        response = translate_text(response, target_language=request.target_language)
        
    return {"response": response}
