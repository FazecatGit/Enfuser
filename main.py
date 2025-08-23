
import sys
from src.translator import Translator

def main():
    while True:
        target_lang = input("Enter target language code (default JA) or press 'q' to quit: ") or "JA"
        translator = Translator(target_lang)
        if target_lang.lower() == 'q':
            break

        should_clear_cache = input("Do you want to clear the cache? (y/n): ")
        if should_clear_cache.lower() == 'y':
            translator.clear_cache()  

        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
        else:
            text = input("Enter text to translate: ")

        translated = translator.translate(text)
        print("\nTranslated text:", translated)

if __name__ == "__main__":
    main()
