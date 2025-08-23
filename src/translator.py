import os
import json
from pathlib import Path
import deepl
from dotenv import load_dotenv

load_dotenv()

class Translator:
    def __init__(self, target_lang="JA"):
        self.target_lang = target_lang.upper()
        self.translator = deepl.Translator(os.getenv("DEEPL_API_KEY"))
        self.cache_file = Path(__file__).parent / "translation_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self):
        """Load cache from JSON file, initialize empty dict if file missing or empty."""
        if self.cache_file.exists() and self.cache_file.stat().st_size > 0:
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("[Warning] Cache file corrupted, initializing empty cache.")
                return {}
        return {}

    def _save_cache(self):
        """Save the in-memory cache to the JSON file."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error writing cache: {e}")

    def translate(self, text):
        """Translate text, using cache if available."""
        key = f"{text.strip().lower()}_{self.target_lang}"
        if key in self.cache:
            print("[cache hit]")
            return self.cache[key]

        result = self.translator.translate_text(text, target_lang=self.target_lang)
        self.cache[key] = result.text
        self._save_cache()
        return result.text


    def clear_cache(self):
        """Clear the translation cache."""
        self.cache = {}
        self._save_cache()
        print("[cache cleared]")

    def choose_language(self):
        languages = ["JA", "ZH", "RU", "DE", "KO"]
        print("Choose target language:")
        for i, lang in enumerate(languages, 1):
            print(f"{i}. {lang}")
        choice = input("Enter the number of your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(languages):
            self.target_lang = languages[int(choice) - 1]
        print(f"Target language set to: {self.target_lang}")
