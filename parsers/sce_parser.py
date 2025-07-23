# parsers/sce_parser.py

import re

def parse_sce(text: str) -> dict:
    """
    Extrait les informations clés d'une facture Southern California Edison.
    Champs retournés :
      - supplier
      - energy
      - date
      - invoice_number
      - receiver_name
      - receiver_address
    À adapter selon le format exact des factures SCE.
    """
    data = {
        "supplier": "SouthernCaliforniaEdison",
        "energy": None,
        "date": None,
        "invoice_number": None,
        "receiver_name": None,
        "receiver_address": None
    }

    # Type d'énergie (par exemple "Electric" ou "Gas")
    m = re.search(r"(electric|gas)", text, re.IGNORECASE)
    if m:
        data["energy"] = m.group(1).capitalize()

    # Date de la facture (ex : Bill Date: MM/DD/YYYY)
    m = re.search(r"Bill Date[:\s]+(\d{1,2}/\d{1,2}/\d{4})", text)
    if m:
        data["date"] = m.group(1)

    # Numéro de facture (ex : Invoice Number: 12345678)
    m = re.search(r"Invoice Number[:\s]+([A-Z0-9-]+)", text)
    if m:
        data["invoice_number"] = m.group(1).strip()

    # Nom du destinataire (ex : Account Name: John Doe)
    m = re.search(r"Account Name[:\s]+(.+)", text)
    if m:
        data["receiver_name"] = m.group(1).strip()

    # Adresse du destinataire (ex : Service Address: 123 Main St, Anytown CA 90001)
    m = re.search(r"Service Address[:\s]+(.+)", text)
    if m:
        data["receiver_address"] = m.group(1).strip()

    return data
