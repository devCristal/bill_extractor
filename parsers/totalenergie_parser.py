# parsers/totalenergie_parser.py

import re

def parse_totalenergie(text: str) -> dict:
    """
    Extrait les informations d'identification d'une facture TotalEnergies :
      - supplier
      - energy
      - date
      - invoice_number
      - receiver_name
      - receiver_address
    """
    data = {
        "supplier": "TotalEnergie",
        "energy": None,
        "date": None,
        "invoice_number": None,
        "receiver_name": None,
        "receiver_address": None
    }

    # Type d'énergie (électricité ou gaz)
    m = re.search(r"(électricité|gaz)", text, re.IGNORECASE)
    if m:
        data["energy"] = m.group(1).capitalize()

    # Date de la facture
    m = re.search(r"Date\s*:\s*(\d{2}/\d{2}/\d{4})", text)
    if m:
        data["date"] = m.group(1)

    # Numéro de facture
    m = re.search(r"Référence facture\s*:\s*([A-Z0-9]+)", text)
    if m:
        data["invoice_number"] = m.group(1).strip()

    # Nom du destinataire : première ligne après "N° de TVA"
    m = re.search(r"N° de TVA[^\n]*\n(.+)", text)
    if m:
        data["receiver_name"] = m.group(1).rstrip(" -").strip()

    # Adresse du destinataire : deux lignes  après trois sauts de ligne post "N° de TVA"
    m = re.search(r"N° de TVA[^\n]*\n(?:.+\n){3}(.+)\n(.+)", text)
    if m:
        street, city = m.group(1).strip(), m.group(2).strip()
        data["receiver_address"] = f"{street} / {city}"

    return data
