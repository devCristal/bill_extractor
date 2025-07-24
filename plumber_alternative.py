from PyPDF2 import PdfReader
from pathlib import Path

def read_pdf_with_pypdf2(path: Path) -> str:
    reader = PdfReader(str(path))
    text = []
    for page in reader.pages:
        # extract_text() renvoie une string ou None
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n\n".join(text)

if __name__ == "__main__":
    pdf_path = Path(r"C:\Users\TomCHARON\OneDrive - MEOGROUP\Documents\App\bill_extractor\factures\202501 Edison.pdf")
    contenu = read_pdf_with_pypdf2(pdf_path)
    print("=== Contenu brut de la facture ===\n")
    print(contenu)
