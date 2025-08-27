import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from pynput import keyboard

HOTKEY_FILE = "src/keyboard_hotkeys.json"

# Load/save hotkeys
def load_hotkeys():
    try:
        with open(HOTKEY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return {}

def save_hotkeys(hotkeys):
    try:
        with open(HOTKEY_FILE, "w") as f:
            json.dump(hotkeys, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Hotkey listener
class HotkeyManager:
    def __init__(self, hotkeys, callback):
        self.hotkeys = hotkeys
        self.callback = callback
        self.listener = None

    def start(self):
        if self.listener:
            self.listener.stop()

        hotkey_mapping = {}
        for func, combo in self.hotkeys.items():
            combo_pynput = combo.lower()
            combo_pynput = combo_pynput.replace("ctrl", "<ctrl>")
            combo_pynput = combo_pynput.replace("shift", "<shift>")
            combo_pynput = combo_pynput.replace("alt", "<alt>")
            hotkey_mapping[combo_pynput] = lambda f=func: self.callback(f)

        self.listener = keyboard.GlobalHotKeys(hotkey_mapping)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def update_hotkeys(self, new_hotkeys):
        self.hotkeys = new_hotkeys
        self.start()

# GUI editor
class HotkeyEditor(tk.Toplevel):
    def __init__(self, master, hotkeys, rebind_callback):
        super().__init__(master)
        self.title("Hotkey Editor")
        self.hotkeys = hotkeys
        self.rebind_callback = rebind_callback
        self.create_widgets()

    def create_widgets(self):
        for i, (func, hotkey) in enumerate(self.hotkeys.items()):
            tk.Label(self, text=func.capitalize()).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            tk.Label(self, text=hotkey).grid(row=i, column=1, padx=5, pady=5)
            tk.Button(self, text="Change", command=lambda f=func: self.change_hotkey(f)).grid(row=i, column=2, padx=5, pady=5)

    def change_hotkey(self, func):
        new_hotkey = simpledialog.askstring("Change Hotkey", f"Enter new hotkey for {func.capitalize()}:")
        if new_hotkey:
            self.hotkeys[func] = new_hotkey
            save_hotkeys(self.hotkeys)
            self.rebind_callback(self.hotkeys)
            messagebox.showinfo("Success", f"Hotkey for {func.capitalize()} changed to {new_hotkey}.")
            self.destroy()
            HotkeyEditor(self.master, self.hotkeys, self.rebind_callback)  # refresh :)