
import sys
from src.translator import * #need to make

def main():
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        text = input("Enter text to convert to translate: ")


    translated = translated_text(text)
    print("\nTranslated text:", translated)

if __name__ == "__main__":
    main()