import tkinter as tk
from tkinter import messagebox 
from src.translator import Translator

translator = Translator()

class GUI:
    def __init__(self, master):
        self.master = master
        self.translator = translator
        self.translator.target_lang = "JA"

        self.setup_controls()
        self.setup_text_frames()

    def setup_controls(self):
        top_frame = tk.Frame(self.master)
        top_frame.pack(pady=10)

        self.setup_source_language(top_frame)

        self.translate_button = tk.Button(top_frame, text="Translate", command=self.translate_text)
        self.translate_button.pack(side=tk.LEFT, padx=5)

        self.clear_cache_button = tk.Button(top_frame, text="Clear Cache", command=self.clear_cache)
        self.clear_cache_button.pack(side=tk.LEFT, padx=5)

        self.swap_button = tk.Button(top_frame, text="⇄ Swap", command=self.swap_languages)
        self.swap_button.pack(side=tk.LEFT, padx=5)
        
        self.lang_ver = tk.StringVar(self.master)
        self.lang_ver.set(self.translator.target_lang)
        self.lang_menu = tk.OptionMenu(top_frame, self.lang_ver, *["JA", "EN", "KO", "ZH"])
        self.lang_menu.pack(side=tk.LEFT, padx=5)

    def setup_source_language(self, parent_frame):
        self.source_lang_ver = tk.StringVar(self.master)
        self.source_lang_ver.set("EN")
        self.source_menu = tk.OptionMenu(parent_frame, self.source_lang_ver, *["EN", "JA", "KO", "ZH"])
        self.source_menu.pack(side=tk.LEFT, padx=5)

        
    def setup_text_frames(self):
        text_frames = tk.Frame(self.master)
        text_frames.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.label = tk.Label(text_frames, text="Enter text to translate:")
        self.label.pack(anchor="w") 

        self.input_text = tk.Text(text_frames, wrap="word")
        self.input_text.pack(side=tk.LEFT, fill="both", expand=True)

        self.output_text = tk.Text(text_frames, wrap="word")
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)

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
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Translator GUI")
    gui = GUI(root)
    root.mainloop()
