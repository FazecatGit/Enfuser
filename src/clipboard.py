import pyperclip

class ClipboardManager:

    @staticmethod
    def get_text():
        return pyperclip.paste()
    
    @staticmethod
    def set_text(text: str):
        pyperclip.copy(text)