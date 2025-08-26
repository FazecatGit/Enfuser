import os
import json
from pathlib import Path
import deepl
from dotenv import load_dotenv

load_dotenv()

class Translator:
    def __init__(self, target_lang="JA", source_lang="EN"):
        self.valid_languages = ["JA", "ZH", "RU", "DE", "KO", "EN"] 
        self.target_lang = target_lang.upper()
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
        self.source_lang = source_lang.upper() 
        self.cache_file = Path(__file__).parent / "translation_cache.json"
        self.cache = self._load_cache()
        self.valid_languages = ["JA", "ZH", "RU", "DE", "KO", "EN"]
        self.target_lang = target_lang if target_lang in self.valid_languages else "EN"

    def _load_cache(self):
        if self.cache_file.exists() and self.cache_file.stat().st_size > 0:
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[Warning] Cache file corrupted, initializing empty cache.")
                return {}
        return {}

    def _save_cache(self):
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing cache: {e}")

    def translate(self, text):
        key = f"{text.strip().lower()}_{self.source_lang}_{self.target_lang}"
        if key in self.cache:
            return self.cache[key]

        try:
            result = self.translator.translate_text(text, target_lang=self.target_lang)
            translated = result.text
        except Exception:
            translated = f"[{self.target_lang}] {text}"

        self.cache[key] = translated
        self._save_cache()
        return translated

    def clear_cache(self):
        self.cache = {}
        self._save_cache()
        print("[cache cleared]")

    def choose_language(self):
        valid_languages = ["JA", "ZH", "RU", "DE", "KO"]
        lang = input(f"Enter target language code {valid_languages} (default {self.target_lang}): ") or self.target_lang
        if lang in valid_languages:
            self.target_lang = lang.upper()
        else:
            print(f"Invalid language code. Keeping default: {self.target_lang}")

        return self.target_lang

    def translate_from(self, text, source_lang):
        key = f"{text.strip().lower()}_{self.target_lang}"
        if key in self.cache:
            print("[cache hit]")
            return self.cache[key]

        result = self.translator.translate_text(text, source_lang=source_lang, target_lang=self.target_lang)
        self.cache[key] = result.text
        self._save_cache()
        return result.text
    
    def swap_languages(self):
        self.source_lang, self.target_lang = self.target_lang, self.source_lang

    def set_target_language(self, lang_code):
        if lang_code in self.valid_languages:
            self.target_lang = lang_code
        else:
            raise ValueError(f"Invalid language code: {lang_code}")
        
    def get_cache_contents(self):
        return "\n".join(f"{k} -> {v}" for k, v in self.cache.items())