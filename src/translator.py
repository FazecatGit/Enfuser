from pathlib import Path
import deepl
import os
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
    key = f"{text.strip().lower()}_{target_lang.upper()}"
    
    cache_file = Path(__file__).parent / "translation_cache.json"
    
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            if cache_file.stat().st_size == 0:
                cache = {}
            else:
                cache = json.load(f)
    else:
        cache_file.write_text("{}", encoding="utf-8")
        cache = {}
    
    cache[key] = translated_text

    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f"[cache saved] {cache_file.resolve()}")
    except Exception as e:
        print(f"Error writing cache: {e}")


def get_cached_translation(text, target_lang="JA"):
    key = f"{text}_{target_lang}"
    cache_file = Path(__file__).parent / "translation_cache.json"

    if cache_file.exists():
        if cache_file.stat().st_size == 0:
            return None
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
            return cache.get(key)
    return None

def clear_cache():
    cache_file = Path(__file__).parent / "translation_cache.json"
    if cache_file.exists():
        cache_file.unlink()
        print(f"[cache cleared] {cache_file.resolve()}")

def choose_language():
    languages = ["JA", "ZH", "RU", "DE", "KO"]
    print("Choose target language:")
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang}")
    choice = input("Enter the number of your choice: ")
    if choice.isdigit() and 1 <= int(choice) <= len(languages):
        return languages[int(choice) - 1]
    print("Invalid choice, defaulting to JA.")
    return "JA"
