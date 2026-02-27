from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.embedding_model import embedding_single
from app.services.faiss_store_db import search_index
from app.services.language_detect import detect_language
from app.services.translate import translate_text
from app.config import settings
import numpy as np

router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    query: str
    output_language: Optional[str] = None  # "en" or "ja"; if omitted, use query language


@router.post("")
async def generate_response(request: GenerateRequest):
    query_embedding = np.array([embedding_single(request.query)], dtype=np.float32)
    results = search_index(query_embedding, top_k=settings.TOP_K)

    context = "\n\n".join([t for t, _ in results]) if results else "No relevant documents found."
    sources = [t for t, _ in results]
    source_block = "\n".join([f"- {s}" for s in sources]) if sources else "- None"
    mock_response = (
        "Answer (mock LLM):\n"
        f"Based on the retrieved documents text, It is a response based on your query.\n\n"
        f"Query: {request.query}\n\n"
        f"Context:\n{context}\n\n"
        f"Sources:\n{source_block}\n\n"
        "(Mock response: In Production, LLM  generate this.)"
    )

    # Bilingual output: same as query language (or explicit output_language)
    target_lang = request.output_language if request.output_language else detect_language(request.query)
    response = mock_response
    if target_lang != "en":
        response = translate_text(response, target=target_lang)

    return {"response": response, "sources": sources}