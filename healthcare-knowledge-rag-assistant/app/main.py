
from fastapi import FastAPI, Depends
from app.config import settings
from app.auth_dependencies import verify_api_key
from app.routes import ingest, retrieve, generate


app = FastAPI(title="Healthcare Knowledge RAG Assistant", version="1.0")

app.include_router(ingest.router, dependencies=[Depends(verify_api_key)])
app.include_router(retrieve.router, dependencies=[Depends(verify_api_key)])
app.include_router(generate.router, dependencies=[Depends(verify_api_key)])

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

