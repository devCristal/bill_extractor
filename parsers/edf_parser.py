# parsers/edf_parser.py

import re

def parse_edf(text: str) -> dict:
    """
    Extrait les informations clés d'une facture EDF.
    Retourne un dict avec les champs :
      - supplier
      - energy
      - date
      - invoice_number
      - receiver_name
      - receiver_address
      - meter_id
      - PDL_address
      - volume_kwh
      - DSO
      - amount_excl_VAT
      - VAT_amount
      - amount_incl_VAT
    """
    data = {
        "supplier": "EDF",
        "energy": None,
        "date": None,
        "invoice_number": None,
        "receiver_name": None,
        "receiver_address": None,
        "meter_id": None,
        "PDL_address": None,
        "volume_kwh": None,
        "DSO": None,
        "amount_excl_VAT": None,
        "VAT_amount": None,
        "amount_incl_VAT": None
    }

    # Type d'énergie
    m = re.search(r'(Electricité|Gaz)[^\n]*', text)
    if m:
        data["energy"] = m.group(0).strip()

    # Date de la facture
    m = re.search(r'Facture du\s+(\d{2}/\d{2}/\d{4})', text)
    if m:
        data["date"] = m.group(1)

    # Numéro de facture
    m = re.search(r'Facture du\s+\d{2}/\d{2}/\d{4}\s+n°\s*([0-9A-Z-]+)', text)
    if m:
        data["invoice_number"] = m.group(1)

    # Nom du destinataire
    m = re.search(r"A l'attention de\s*(.+)", text)
    if m:
        data["receiver_name"] = m.group(1).strip()

    # Adresse du destinataire (3 lignes sous "A l'attention de")
    m = re.search(r"A l'attention de[^\n]*\n(.+)\n(.+)\n(.+)", text)
    if m:
        data["receiver_address"] = " / ".join(g.strip() for g in m.groups())

    # Identifiant de comptage
    m = re.search(r'Identifiant de comptage\s*[:\-]?\s*(\d+)', text)
    if m:
        data["meter_id"] = m.group(1)

    # Adresse du point de livraison (ligne sous "Contrat")
    m = re.search(r'Contrat[^\n]*\n(.+ \d{5} .+)', text)
    if m:
        data["PDL_address"] = m.group(1).strip()

    # Consommation kWh
    m = re.search(r'Consommation .*?([\d\s]+kWh)', text)
    if m:
        data["volume_kwh"] = m.group(1).replace(" ", "")

    # Gestionnaire du réseau (DSO)
    m = re.search(r'\b(GRDF|Enedis)\b', text)
    if m:
        data["DSO"] = m.group(1)

    # Montant Hors TVA
    m = re.search(r'Montant Hors TVA\s*([\d\s,]+)\s?€', text)
    if m:
        data["amount_excl_VAT"] = m.group(1).replace(" ", "").replace(",", ".")

    # Montant TVA
    m = re.search(r'Montant TVA.*?([\d\s,]+)\s?€', text)
    if m:
        data["VAT_amount"] = m.group(1).replace(" ", "").replace(",", ".")

    # Montant TTC
    m = re.search(r'Facture TTC\s*([\d\s,]+)\s?€', text)
    if m:
        data["amount_incl_VAT"] = m.group(1).replace(" ", "").replace(",", ".")

    return data
