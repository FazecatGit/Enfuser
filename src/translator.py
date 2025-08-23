import deepl
import os

auth_key = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

def translate_text(text, target_lang="EN"):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text