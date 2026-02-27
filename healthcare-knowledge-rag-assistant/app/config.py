from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # X-API-Key for Auth in Header
    API_KEY: str = "my_secret_api_key"
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    FAISS_INDEX_PATH: str = "faiss_index"
    TOP_K: int = 3
    
    class Config:
        env_file = ".env"
        
settings = Settings()
    