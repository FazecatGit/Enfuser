import pytesseract
import pyautogui
from PIL import Image
import sys
import subprocess

class OCRScreenshot:
    def __init__(self,translator ,lang="eng"):
        self.lang = lang
        self.translator = translator

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
        
    def capture_text_from_file(self, image_path: str) -> str:
        """OCR text from an image file."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=self.lang)
            return text
        except Exception as e:
            print(f"Error capturing text from file: {e}")
            return ""

    def capture_and_translate_region(self, return_original) -> str:
        """
        Capture fullscreen region (click-and-drag on Linux using slop, full screen fallback on others),
        perform OCR, then translate using the assigned translator.
        """
        try:
            # Step 1: Get region coordinates
            if sys.platform.startswith("linux"):
                # Use slop for selection (install with sudo apt install slop)
                coords = subprocess.check_output("slop -f '%x %y %w %h'", shell=True).decode().strip()
                x, y, w, h = map(int, coords.split())
            else:
                # On Windows/macOS: full screen
                screen = pyautogui.size()
                x, y, w, h = 0, 0, screen.width, screen.height

            # Step 2: Screenshot
            img = pyautogui.screenshot(region=(x, y, w, h))

            # Step 3: OCR
            ocr_text = pytesseract.image_to_string(img, lang=self.lang)
            if not ocr_text.strip():
                print("No text detected in the selected region.")
                return ""

            # Step 4: Translate
            if self.translator:
                translated_text = self.translator.translate(ocr_text)
            else:
                translated_text = ocr_text

            if return_original:
                return ocr_text, translated_text
            else:
                return translated_text

        except subprocess.CalledProcessError:
            print("Region selection cancelled")
            return ""
        except Exception as e:
            print(f"Error capturing and translating region: {e}")
            return ""
            

