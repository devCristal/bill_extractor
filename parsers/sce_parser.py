import re
from datetime import datetime

def parse_sce(text: str) -> dict:
    """
    Extrait des factures Southern California Edison :
      • supplier           : "SouthernCaliforniaEdison"
      • date               : date d'émission (après 'Due by'), format DD/MM/YYYY
      • receiver_name      : nom du destinataire (ligne avant '/ Page')
      • receiver_address   : adresse du destinataire (lignes après 'Due by')
      • invoice_number     : identifiant de la facture (STMT…), ou compte client
      • energy             : 'gas' ou 'electricity'
      • meter_point_id     : numéro du compteur (POD-ID)
      • service_address    : adresse de service (avant le POD-ID)
    """
    data = {
        "supplier": "SouthernCaliforniaEdison",
        "date": None,
        "receiver_name": None,
        "receiver_address": None,
        "invoice_number": None,
        "energy": None,
        "meter_point_id": None,
        "service_address": None,
    }

    def to_fr_date(us_date: str) -> str:
        fmt = "%m/%d/%y" if len(us_date.split("/")[-1]) == 2 else "%m/%d/%Y"
        dt = datetime.strptime(us_date, fmt)
        return dt.strftime("%d/%m/%Y")

    # 1) Date et adresse destinataire
    m_due = re.search(
        r"Due\s+by[^\n]*?([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text, re.IGNORECASE
    )
    if m_due:
        data["date"] = to_fr_date(m_due.group(1))
        tail = text[m_due.end():].splitlines()
        lines = [l.strip() for l in tail if l.strip()]
        for i, ln in enumerate(lines):
            if re.match(r"^\d", ln):
                next_line = lines[i+1] if i+1 < len(lines) else ""
                data["receiver_address"] = f"{ln}, {next_line}".strip(", ")
                break

    # 2) Nom du destinataire
    m_recv = re.search(
        r"^([A-Z0-9 &\-\.'\,]+?)\s*/\s*Page",
        text, re.MULTILINE | re.IGNORECASE
    )
    if m_recv:
        data["receiver_name"] = m_recv.group(1).strip()

    # 3) Numéro de facture ou de compte
    m_stmt = re.search(r"\b(STMT\s*[0-9]{6,8}(?:\s*P[0-9]+)?)\b", text, re.IGNORECASE)
    if m_stmt:
        data["invoice_number"] = m_stmt.group(1).strip()
    else:
        m_acc = re.search(r"\b(\d{12})\b", text)
        if m_acc:
            data["invoice_number"] = m_acc.group(1)

    # 4) Type d'énergie
    if re.search(r"\bgas\b", text, re.IGNORECASE):
        data["energy"] = "gas"
    elif re.search(r"\belectricity\b", text, re.IGNORECASE):
        data["energy"] = "electricity"

    # 5) Extraction du POD-ID et de l'adresse de service
    # On utilise un regex non-greedy avant le groupe, et on capture à la fois l'adresse et le POD
    m_service = re.search(
        r"Service address\s+(.+?)\s+(\d{12,20})(?!\d)",
        text, re.IGNORECASE
    )
    if m_service:
        data["service_address"] = m_service.group(1).strip()
        data["meter_point_id"] = m_service.group(2)

    return data
