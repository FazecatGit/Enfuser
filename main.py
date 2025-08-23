
import sys
from src.translator import * #need to make

def main():
    while True:

        target_language = choose_language()
        print(f"Selected target language: {target_language}")

        text = input("Enter text to translate (or 'q' to quit): ").strip()
        if text.lower() == "q":
            break
        
        should_clear_cache = input("Clear cache? (y/n): ").strip().lower() == "y"
        if should_clear_cache:
            clear_cache()

        translated = translate_text(text, target_lang=target_language)
        print("\nTranslated text:", translated)

if __name__ == "__main__":
    main()