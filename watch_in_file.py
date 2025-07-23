# inspect_invoice.py

import pdfplumber
from pathlib import Path

def main():
    # 1) Chemin du dossier contenant tes factures
    folder = Path(r"C:\Users\TomCHARON\OneDrive - MEOGROUP\Documents\App\extract_test\extract_test\factures")
    if not folder.exists():
        print(f"❌ Le dossier n'existe pas : {folder}")
        return

    # 2) Liste les fichiers PDF disponibles
    pdfs = list(folder.glob("*.pdf"))
    if not pdfs:
        print("⚠️ Aucun PDF dans", folder)
        return

    print("PDF disponibles :")
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"  {i}. {pdf_path.name}")

    # 3) Demande à l'utilisateur de choisir un index
    choix = input("Entrez le numéro du PDF à afficher : ")
    try:
        idx = int(choix) - 1
        pdf_path = pdfs[idx]
    except (ValueError, IndexError):
        print("❌ Choix invalide")
        return

    # 4) Extraction et affichage
    print(f"\n--- Contenu brut de {pdf_path.name} ---\n")
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            print(f"--- Page {page_num} ---")
            print(text)
            print()
    print("--- FIN ---")

if __name__ == "__main__":
    main()
