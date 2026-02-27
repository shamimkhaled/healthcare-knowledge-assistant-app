from langdetect  import LangDetectException, detect

def detect_language(text: str) -> str:
    try:
        code = detect(text)
        return "ja" if code == "ja" else "en"
    except LangDetectException:
        return "en"
    
    
    