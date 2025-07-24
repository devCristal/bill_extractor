#!/usr/bin/env python3

from pathlib import Path
import fitz               # PyMuPDF
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\TomCHARON\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)

def extract_text_with_ocr(pdf_path: Path):
    """
    Pour chaque page, on la transforme en pixmap via PyMuPDF,
    puis on OCRise via pytesseract.
    """
    doc = fitz.open(str(pdf_path))
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(dpi=300)
        # Crée une image PIL à partir des octets
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img, lang="fra+eng")
        print(f"--- Page {i} ---\n{text}\n")

def main():
    # Chemin direct vers ta facture SCE
    pdf_path = Path(r"C:\Users\TomCHARON\OneDrive - MEOGROUP\Documents\App\bill_extractor\factures\202501 Edison.pdf")
    if not pdf_path.exists():
        print(f"❌ Fichier introuvable : {pdf_path}")
        return

    print(f"📄 OCR de : {pdf_path}\n")
    extract_text_with_ocr(pdf_path)

if __name__ == "__main__":
    main()
