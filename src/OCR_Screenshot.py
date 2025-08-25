import pytesseract
import pyautogui
from PIL import Image

class OCRScreenshot:
    def __init__(self, lang="eng"):
        self.lang = lang

    def set_lang(self, lang_code: str):
        self.lang = lang_code

    def capture_text(self, region=None) -> str:
        try:
            screenshot = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(screenshot, lang=self.lang)
            return text
        except Exception as e:
            print(f"Error capturing text: {e}")
            return ""

    def capture_text_from_file(self, image_path: str) -> str:
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.lang)
            return text
        except Exception as e:
            print(f"Error capturing text from file: {e}")
            return ""
        