import sys
from src.translator import Translator
import tkinter as tk
from src.gui import GUI 
from src.clipboard import ClipboardManager
from src.keyboard_hotkeys import load_hotkeys, HotkeyManager

def run_function(func_name):
    if func_name == "capture_full":
        gui.ocr_translate_screenshot()
    elif func_name == "capture_region":
        gui.translate_screenshot_region()
    elif func_name == "translate":
        gui.translate_text()
    elif func_name == "swap":
        gui.swap_languages()
    elif func_name == "view_cache":
        gui.view_cache()
    elif func_name == "clear_cache":
        gui.clear_cache()
    elif func_name == "clipboard":
        gui.translate_clipboard()


def handle_language_selection(translator):
    target_lang = translator.choose_language()
    if target_lang.lower() == "q":
        return None
    translator.target_lang = target_lang
    return target_lang

def handle_clear_cache(translator):
    should_clear_cache = input("Clear the cache? (y/n): ").strip().lower()
    if should_clear_cache == "y":
        translator.clear_cache()
        print("Cache cleared!\n")

def handle_clipboard_translation(translator):
    if input("Translate from clipboard? (y/n): ").strip().lower() == "y":
        text = ClipboardManager.get_text()
        translated = translator.translate(text)
        print(f"\nTranslated clipboard text ({translator.target_lang}): {translated}")

def handle_text_translation(translator):
    text = input("Enter text to translate: ").strip()
    if text.lower() == "q":
        return None

    translated = translator.translate(text)
    print(f"\nTranslated text ({translator.target_lang}): {translated}")

    source_lang = input("Translate from specific source? (e.g. JA/EN or press Enter to skip): ").strip().lower()
    if source_lang == "q":
        print("Goodbye!")
        return None
    elif source_lang:
        translated_from = translator.translate_from(text, source_lang=source_lang)
        print(f"\nTranslated text (from {source_lang}): {translated_from}")

    return text

def main():
    translator = Translator()
    while True:
        target_lang = handle_language_selection(translator)
        if target_lang is None:
            break

        handle_clipboard_translation(translator)
        handle_clear_cache(translator)

        if len(sys.argv) > 1:
            text = " ".join(sys.argv[1:])
            sys.argv = [sys.argv[0]]
        else:
            text = handle_text_translation(translator)
            if text is None:
                break

        print("\n---\n")

if __name__ == "__main__":
    mode = input("Choose mode: CLI or GUI (c/g): ").strip().lower()
    if mode == "c":
        main()
    elif mode == "g":
        root = tk.Tk()
        root.title("Translator GUI")
        
        # Load hotkeys
        hotkeys = load_hotkeys()
        
        # Create GUI first with a temporary callback
        gui = GUI(root, hotkeys, lambda new_hotkeys: None)
        
        # Create hotkey manager with hotkeys and callback to run GUI functions
        hotkey_manager = HotkeyManager(hotkeys, run_function)
        hotkey_manager.start()
        
        # Now update GUI callback so it can rebind hotkeys if needed
        gui.rebind_callback = lambda new_hotkeys: hotkey_manager.update_hotkeys(new_hotkeys)

        root.mainloop()

