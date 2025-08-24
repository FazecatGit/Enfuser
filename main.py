
import sys
from src.translator import Translator
import tkinter as tk
from src.gui import GUI 

def main():
    translator = Translator()

    print("Welcome to Immerser Translator!")
    print("Type 'q' anytime to quit.\n")

    while True:
        target_lang = translator.choose_language()
        if target_lang.lower() == "q":
            print("Goodbye!")
            break
        translator.target_lang = target_lang

        should_clear_cache = input("Clear the cache? (y/n): ").strip().lower()
        if should_clear_cache == "q":
            print("Goodbye!")
            break
        elif should_clear_cache == "y":
            translator.clear_cache()
            print("Cache cleared!\n")

        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
            sys.argv = [sys.argv[0]]  # reset so it doesn’t loop forever with same args
        else:
            text = input("Enter text to translate: ").strip()

        if text.lower() == "q":
            print("Goodbye!")
            break


        translated = translator.translate(text)
        print(f"\nTranslated text ({translator.target_lang}): {translated}")


        source_lang = input("Translate from specific source? (e.g. JA/EN or press Enter to skip): ").strip().upper()
        if source_lang:
            translated_from = translator.translate_from(text, source_lang=source_lang)
            print(f"\nTranslated text (from {source_lang}): {translated_from}")

        print("\n---\n")

if __name__ == "__main__":
    mode = input("Choose mode: CLI or GUI (c/g): ").strip().lower()
    if mode == "c":
        main()  # CLI loop
    elif mode == "g":
        root = tk.Tk()
        root.title("Translator GUI")
        gui = GUI(root)
        root.mainloop()