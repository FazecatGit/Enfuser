import tkinter as tk
from tkinter import messagebox 
from src.translator import Translator
from src.clipboard import ClipboardManager
from src.OCR_Screenshot import OCRScreenshot


translator = Translator()

class GUI:
    def __init__(self, master):
        self.valid_languages = ["JA", "ZH", "RU", "DE", "KO", "EN"]
        self.master = master
        self.translator = translator
        self.translator.target_lang = "JA"
        self.ocr = OCRScreenshot(translator=self.translator, lang="eng")
        self.master.focus_force()
        self.master.bind("<u>", self.on_hotkey)

        self.setup_controls()
        self.setup_text_frames()

    def setup_controls(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(pady=10)

        #button methods
        self.setup_source_language()
        self.setup_translate_button()
        self.setup_clear_cache_button()
        self.setup_swap_button()
        self.setup_target_language_menu()
        self.setup_translate_clipboard()
        self.setup_toggle_mode()
        self.setup_ocr_translate_screenshot()
        self.setup_hotkey_menu()


    def setup_translate_button(self):
        self.translate_button = tk.Button(self.top_frame, text="Translate", command=self.translate_text)
        self.translate_button.pack(side=tk.LEFT, padx=5)

    def setup_clear_cache_button(self):
        self.clear_cache_button = tk.Button(self.top_frame, text="Clear Cache", command=self.clear_cache)
        self.clear_cache_button.pack(side=tk.LEFT, padx=5)

    def setup_swap_button(self):
        self.swap_button = tk.Button(self.top_frame, text="⇄ Swap", command=self.swap_languages)
        self.swap_button.pack(side=tk.LEFT, padx=5)

    def setup_target_language_menu(self):
        self.lang_ver = tk.StringVar(self.master)
        self.lang_ver.set(self.translator.target_lang)

        def on_lang_change(*args):
            try:
                self.translator.set_target_language(self.lang_ver.get())
            except ValueError as e:
                print(e)

        self.lang_ver.trace_add("write", on_lang_change)

        self.lang_menu = tk.OptionMenu(self.top_frame, self.lang_ver, *self.translator.valid_languages)
        self.lang_menu.pack(side=tk.LEFT, padx=5)

    def setup_source_language(self):
        self.source_lang_ver = tk.StringVar(self.master)
        self.source_lang_ver.set("EN")

        self.source_menu = tk.OptionMenu(self.top_frame, self.source_lang_ver, *self.valid_languages)
        self.source_menu.pack(side=tk.LEFT, padx=5)

        def on_source_change(*args):
            self.translator.source_lang = self.source_lang_ver.get()

        self.source_lang_ver.trace("w", on_source_change)

    def setup_translate_clipboard(self):
        self.clipboard_button = tk.Button(self.top_frame, text="Clipboard Translate", command=self.translate_clipboard)
        self.clipboard_button.pack(side=tk.LEFT, padx=5)


    def setup_toggle_mode(self):
        self.dark_mode = False
        self.toggle_button = tk.Button(self.master, text="Toggle Dark Mode", command=self.toggle_mode)
        self.toggle_button.pack()

    def setup_text_frames(self):
        text_frames = tk.Frame(self.master)
        text_frames.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label = tk.Label(text_frames, text="Enter text to translate:")
        self.label.pack(anchor="w") 

        self.input_text = tk.Text(text_frames, wrap="word")
        self.input_text.pack(side=tk.LEFT, fill="both", expand=True)

        self.output_text = tk.Text(text_frames, wrap="word")
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)


    def setup_ocr_translate_screenshot(self):
        self.ocr_button = tk.Button(self.top_frame, text="OCR Translate Screenshot", command=self.ocr_translate_screenshot)
        self.ocr_button.pack(side=tk.LEFT, padx=5)


    def setup_hotkey_menu(self):
        self.hotkey_ver = tk.StringVar(self.master)
        self.hotkey_ver.set("Clipboard Hotkey")

        hotkeys = ["ctrl+shift+o", "ctrl+alt+t", "alt+q"]

        self.hotkey_menu = tk.OptionMenu(self.top_frame, self.hotkey_ver, *hotkeys)
        self.hotkey_menu.pack(side=tk.LEFT, padx=5)

    #the gui functions
    def translate_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            return
        self.translator.target_lang = self.lang_ver.get()
        translated = self.translator.translate(text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)

    def swap_languages(self):
        self.translator.swap_languages()
        self.source_lang_ver.set(self.translator.source_lang)
        self.lang_ver.set(self.translator.target_lang)

        input_text = self.input_text.get("1.0", tk.END).rstrip("\n")
        output_text = self.output_text.get("1.0", tk.END).rstrip("\n")

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, output_text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, input_text)

    def clear_cache(self):
        confirm = messagebox.askyesno("Clear Cache" , "Are you sure you want to clear cache")
        if confirm:
            self.translator.clear_cache()
            messagebox.showinfo("Cache Cleared", "Translation has been cleared")

    def translate_clipboard(self):
        text = ClipboardManager.get_text()
        if not text:
            return

        self.translator.target_lang = self.lang_ver.get()
        translated = self.translator.translate(text)

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)

        ClipboardManager.set_text(translated)

    # dark mode enabler 

    def enable_dark_mode(self):
        bg = "#1e1e1e"
        fg = "#ffffff"
        self.master.configure(bg=bg)
        widgets = [self.input_text, self.output_text, self.label,
                self.translate_button, self.clear_cache_button, self.swap_button,
                self.toggle_button, self.lang_menu, self.source_menu]
        for w in widgets:
            try:
                w.configure(bg=bg, fg=fg, insertbackground=fg)
            except:
                pass 

    
    def enable_light_mode(self):
        bg = "#ffffff"
        fg = "#000000"
        self.master.configure(bg=bg)
        self.input_text.configure(bg=bg, fg=fg, insertbackground=fg)
        self.output_text.configure(bg=bg, fg=fg, insertbackground=fg)

    def toggle_mode(self):
        if self.dark_mode:
            self.enable_light_mode()
        else:
            self.enable_dark_mode()
        self.dark_mode = not self.dark_mode

    #screenshot

    def ocr_translate_screenshot(self):
        text = self.ocr.capture_text()
        if not text:
            return

        translated = self.translator.translate(text)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)

    def update_hotkey(self, hotkey: str):
        import keyboard
        keyboard.clear_all_hotkeys()
        keyboard.add_hotkey(hotkey, self.ocr_translate_screenshot)

    def translate_screenshot_region(self):
        text = self.ocr.capture_region()
        if not text:
            return
        translated = self.translator.translate(text)
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert(tk.END, text)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, translated)

    def on_hotkey(self, event=None):

        ocr_text = self.ocr.capture_and_translate_region(return_original=True)
        
        if ocr_text:
            original_text, translated_text = ocr_text
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, original_text)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, translated_text)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Translator GUI")
    gui = GUI(root)
    root.mainloop()
