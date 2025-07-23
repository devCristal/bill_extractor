import pandas as pd
import pdfplumber
from pathlib import Path
from parsers.edf_parser import parse_edf
from parsers.totalenergie_parser import parse_totalenergie
# from parsers.engie_parser import parse_engie

def detect_supplier(text: str) -> str | None:
    low = text.lower()
    if "edf" in low:
        return "EDF"
    if "totalenergie" in low or "total energie" in low or "totalenergies" in low:
        return "TotalEnergie"
    return None

def main():
    folder = Path(r"C:\Users\TomCHARON\OneDrive - MEOGROUP\Documents\App\extract_test\extract_test\factures")
    if not folder.exists():
        print(f"❌ Dossier introuvable : {folder}")
        return

    records = []                         # <-- 1) Liste vide

    for pdf_path in folder.glob("*.pdf"):
        print(f"\n--- Lecture de : {pdf_path.name} ---")
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)

        supplier = detect_supplier(text)
        if not supplier:
            print("⚠️ Aucun fournisseur détecté, passe au suivant.")
            continue
        print(f"👉 Fournisseur détecté : {supplier}")

        if supplier == "EDF":
            data = parse_edf(text)
        elif supplier == "TotalEnergie":
            data = parse_totalenergie(text)
        # elif supplier == "Engie":
        #     data = parse_engie(text)
        # else: continue

        data["file_name"] = pdf_path.name
        records.append(data)             # <-- 2) On empile le dict

    if not records:
        print("⚠️ Aucune facture traitée.")
        return

    # 3) En fin de script : on produit l’Excel de toutes les factures
    df = pd.DataFrame(records)
    output = folder / "factures_extraites.xlsx"
    df.to_excel(output, index=False)
    print(f"\n✅ Export terminé : {output}")

if __name__ == "__main__":
    main()
