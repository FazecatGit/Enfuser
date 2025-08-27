import re
import pytesseract
import pyautogui
from PIL import Image, ImageOps
import sys
import subprocess
from src.translator import Translator

translator = Translator()

class OCRScreenshot:
    def __init__(self, translator, lang="eng"):
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

    def capture_region(self) -> str:
        ocr_text, _ = self.capture_and_translate_region(return_original=True)
        return ocr_text

    #placeholder function - redundant
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
        try:
            # Step 1: Get region coordinates
            if sys.platform.startswith("linux"):
                coords = subprocess.check_output("slop -f '%x %y %w %h'", shell=True).decode().strip()
                x, y, w, h = map(int, coords.split())
            else:
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

    def convert_text(self, img):
        gray = ImageOps.grayscale(img)
        bw = gray.point(lambda x: 0 if x < 140 else 255, '1') 

        ocr_text = pytesseract.image_to_string(bw, lang="eng", config='--psm 6')
        ocr_text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', ocr_text)

        return ocr_text 