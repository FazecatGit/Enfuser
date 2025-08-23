import deepl
import os
from pathlib import Path
import json
from dotenv import load_dotenv

load_dotenv()
auth_key = os.getenv("DEEPL_API_KEY")
translator = deepl.Translator(auth_key)

def translate_text(text, target_lang="JA"):
    cached_translation = get_cached_translation(text, target_lang)
    if cached_translation:
        print("[cache hit]")
        return cached_translation
    else:
        result = translator.translate_text(text, target_lang=target_lang)
        cache_translation(text, result.text, target_lang)
        return result.text

def cache_translation(text, translated_text, target_lang="JA"):
    key = f"{text}_{target_lang}"
    cache_file = Path("translation_cache.json")
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
    else:
        cache = {}

    cache[key] = translated_text

    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cached_translation(text, target_lang="JA"):
    key = f"{text}_{target_lang}"
    cache_file = Path("translation_cache.json")
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return cache.get(key)
    return None
