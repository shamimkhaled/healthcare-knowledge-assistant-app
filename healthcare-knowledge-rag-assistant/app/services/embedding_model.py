from sentence_transformers import SentenceTransformer

_model = None

def get_embedding_model(model_name: str = "paraphrase-multilingual-MiniLM-L12-v2") -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def embedding_texts(texts: list[str], model=None) -> list[list[float]]:
    model = model or get_embedding_model()
    return model.encode(texts).tolist()

def embedding_single(text: strr) -> list[float]:
    return embedding_texts([text])[0]


