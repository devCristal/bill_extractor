# main.py
import pandas as pd
import pdfplumber
from pathlib import Path

import fitz               # PyMuPDF
from PIL import Image
import pytesseract        # OCR

# Pointe vers le binaire Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\TomCHARON\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

from parsers.edf_parser import parse_edf
from parsers.totalenergie_parser import parse_totalenergie
from parsers.sce_parser import parse_sce

def extract_text_with_ocr(pdf_path: Path) -> str:
    """
    Convertit chaque page du PDF en image via PyMuPDF, puis fait de l'OCR avec pytesseract.
    """
    doc = fitz.open(str(pdf_path))
    pages_txt = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages_txt.append(pytesseract.image_to_string(img, lang="fra+eng"))
    return "\n\n".join(pages_txt)

import re

def detect_supplier(text: str) -> str | None:
    low = text.lower()

    # 1) Southern California Edison (mot complet ou acronyme SCE)
    if "southern california edison" in low or re.search(r"\bsce\b", low):
        return "SouthernCaliforniaEdison"

    # 2) EDF (mot entier)
    if re.search(r"\bedf\b", low):
        return "EDF"

    # 3) TotalEnergie
    if "totalenergie" in low or "total energie" in low or "totalenergies" in low:
        return "TotalEnergie"

    return None


def main():
    folder = Path(r"C:\Users\TomCHARON\OneDrive - MEOGROUP\Documents\App\bill_extractor\factures")
    if not folder.exists():
        print(f"❌ Dossier introuvable : {folder}")
        return

    records = []
    for pdf_path in folder.glob("*.pdf"):
        print(f"\n--- Lecture de : {pdf_path.name} ---")

        # 1) Extraction de texte natif
        with pdfplumber.open(pdf_path) as pdf:
            native_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        # 2) Première détection fournisseur sur texte natif
        supplier = detect_supplier(native_text)
        text = native_text

        # 3) Si pas détecté ou SCE avec texte vide, on tente l'OCR
        if not supplier or (supplier == "SouthernCaliforniaEdison" and not native_text.strip()):
            print("⚠️ Détection native échouée ou SCE sans texte natif, lancement de l'OCR…")
            ocr_text = extract_text_with_ocr(pdf_path)
            supplier = detect_supplier(ocr_text)
            text = ocr_text

        if not supplier:
            print("⚠️ Aucun fournisseur détecté après OCR, passe au suivant.")
            continue

        print(f"👉 Fournisseur détecté : {supplier}")

        # 4) Parsing selon fournisseur
        if supplier == "EDF":
            data = parse_edf(text)
        elif supplier == "TotalEnergie":
            data = parse_totalenergie(text)
        elif supplier == "SouthernCaliforniaEdison":
            data = parse_sce(text)
        else:
            continue

        data["file_name"] = pdf_path.name
        records.append(data)

    if not records:
        print("⚠️ Aucune facture traitée.")
        return

    # 5) Export Excel
    df = pd.DataFrame(records)
    output = folder / "factures_extraites.xlsx"
    df.to_excel(output, index=False)
    print(f"\n✅ Export terminé : {output}")

if __name__ == "__main__":
    main()
