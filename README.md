# Enfuser

A translator application designed to help you **immerse yourself in a language** by scanning text from your screen or typing it directly.  
The goal is to enhance language learning and provide a simple, user-friendly interface for quick translations.

It also includes a **CLI translator** and plans to integrate advanced features using the DEEPL API.

---

## Features
- Translate text from screen captures or clipboard.  
- Simple GUI with Tkinter.  
- CLI-based translator for quick usage.  
- Modular design: core translation, OCR, and hotkeys are separated for easier maintenance.  

---

## Installation

### 1. Install Python
Ensure you have **Python 3.10+** installed.

```bash
python --version
```
### 2. Clone the repository
```bash
https://github.com/FazecatGit/Enfuser.git
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install system dependencies

Tesseract OCR (required for pytesseract) and slop for screen selection:

Linux:
```bash 
sudo apt install tesseract-ocr
sudo apt install slop
```

### 5. Running the file

go to the root of the file and paste this 
```bash 
uv run main.py
```
you should have either "c" for CLI or "g" for GUI
GUI allows more featues than the CLI at the moment.

Windows: Download installer from Tesseract GitHub

### Notes

The project is has more room to improve and primarily for personal learning and experimentation.

DEEPL API is used for robust translation. Make sure to include your API key in a .env file.

Contributions are welcome once the project is more complete.

I'll slowly be updating till the limitations of the program have been met. 
This is my proper first solo and I know it ain't great but I'll look at it 
and see if theres any way to improve on it. Don't expect much from this.