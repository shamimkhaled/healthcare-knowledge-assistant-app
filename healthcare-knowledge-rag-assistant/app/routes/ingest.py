from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.faiss_store_db import add_to_index, get_metadata
from app.services.embedding_model import embedding_texts, get_embedding_model
from app.services.language_detect import detect_language
from app.config import settings
import numpy as np

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.post("")
async def ingest_document(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only text files are supported.")
    
    content = await file.read()
    text = content.decode("utf-8")
    
    language = detect_language(text)
    embedding_model = get_embedding_model(settings.EMBEDDING_MODEL)
    embedding = embedding_texts([text], model=embedding_model)[0]
    
    metadata_entry = {
        "filename": file.filename,
        "language": language
    }
    
    add_to_index(np.array([embedding]), [metadata_entry])
    
    return {"message": f"Document '{file.filename}' ingested successfully."}
