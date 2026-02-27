from googletrans import Translator
from deep_translator import GoogleTranslator


def translate_text(text: str, target: str) -> str:
    translator = Translator()
    try:
        result = translator.translate(text, dest=target)
        return result.text
    except Exception as e:
        try:
            return GoogleTranslator(source="auto", target=target).translate(text)
        except Exception:
            return f"[Translated to {target}]: {text}"
        
        
        
        
        
