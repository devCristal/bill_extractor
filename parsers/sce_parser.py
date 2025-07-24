import re
from datetime import datetime

def parse_sce(text: str) -> dict:
    """
    Extrait des factures Southern California Edison :
      • supplier (fixe)
      • date d'émission (après 'Due by'), au format DD/MM/YYYY
      • receiver_name     : nom du destinataire (ligne avant '/ Page')
      • receiver_address  : adresse du destinataire (lignes après 'Due by')
      • invoice_number    : identifiant de la facture (STMT…), ou compte client
      • energy            : 'gas' ou 'electricity' si présent dans le texte
    """
    data = {
        "supplier": "SouthernCaliforniaEdison",
        "date": None,
        "receiver_name": None,
        "receiver_address": None,
        "invoice_number": None,
        "energy": None,
    }

    def to_fr_date(us_date: str) -> str:
        fmt = "%m/%d/%y" if len(us_date.split("/")[-1]) == 2 else "%m/%d/%Y"
        dt = datetime.strptime(us_date, fmt)
        return dt.strftime("%d/%m/%Y")

    # 1) Date et adresse
    m_due = re.search(
        r"Due\s+by[^\n]*?([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text,
        re.IGNORECASE
    )
    if m_due:
        data["date"] = to_fr_date(m_due.group(1))
        tail = text[m_due.end():].splitlines()
        lines = [l.strip() for l in tail if l.strip()]
        for i, ln in enumerate(lines):
            if re.match(r"^\d", ln):
                street = ln
                city = lines[i+1] if i+1 < len(lines) else ""
                data["receiver_address"] = f"{street}, {city}".strip(", ")
                break

    # 2) Nom du destinataire
    m_recv = re.search(
        r"^([A-Z0-9 &\-\.'\,]+?)\s*/\s*Page",
        text,
        re.MULTILINE | re.IGNORECASE
    )
    if m_recv:
        data["receiver_name"] = m_recv.group(1).strip()

    # 3) Invoice number (STMT… avec ou sans espace avant suffixe P, ou fallback compte client)
    m_stmt = re.search(
        r"\b(STMT\s*[0-9]{6,8}(?:\s*P[0-9]+)?)\b",
        text,
        re.IGNORECASE
    )
    if m_stmt:
        data["invoice_number"] = m_stmt.group(1).strip()
    else:
        # fallback : numéro de compte client (12 chiffres)
        m_acc = re.search(r"\b(\d{12})\b", text)
        if m_acc:
            data["invoice_number"] = m_acc.group(1)

    # 4) Type d'énergie
    if re.search(r"\bgas\b", text, re.IGNORECASE):
        data["energy"] = "gas"
    elif re.search(r"\belectricity\b", text, re.IGNORECASE):
        data["energy"] = "electricity"

    return data
