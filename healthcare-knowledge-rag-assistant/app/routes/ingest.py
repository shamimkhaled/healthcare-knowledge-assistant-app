from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List
from app.services.faiss_store_db import add_to_index
from app.services.embedding_model import embedding_texts, get_embedding_model
from app.services.language_detect import detect_language
from app.config import settings
import numpy as np

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("")
async def ingest_document(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    embedding_model = get_embedding_model(settings.EMBEDDING_MODEL)
    results = []

    for file in files:
        if not file.filename or not file.filename.lower().endswith(".txt"):
            raise HTTPException(status_code=400, detail="Only .txt files are supported.")

        content = await file.read()
        text = content.decode("utf-8")

        language = detect_language(text)

        # Chunk by paragraphs, then cap size for better retrieval diversity
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: list[str] = []
        max_len = 500
        for para in paragraphs:
            if len(para) <= max_len:
                chunks.append(para)
            else:
                for i in range(0, len(para), max_len):
                    chunk = para[i : i + max_len].strip()
                    if chunk:
                        chunks.append(chunk)
        if not chunks:
            chunks = [text[:max_len]]

        embeddings = embedding_texts(chunks, model=embedding_model)

        metadata_entries = [
            {"filename": file.filename, "language": language, "text": chunk}
            for chunk in chunks
        ]

        add_to_index(np.array(embeddings), metadata_entries)

        results.append(
            {"filename": file.filename, "language": language, "chunks": len(chunks)}
        )

    return {"message": "Ingestion complete.", "files": results}