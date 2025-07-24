import re
from datetime import datetime

def parse_sce(text: str) -> dict:
    """
    Extrait des factures Southern California Edison :
      • supplier (fixe)
      • date d'émission (après 'Due by'), au format DD/MM/YYYY
      • receiver_name : nom du destinataire (ligne avant '/ Page')
      • energy : 'gas' ou 'electricity' si présent dans le texte
    """
    data = {
        "supplier": "SouthernCaliforniaEdison",
        "date": None,
        "receiver_name": None,
        "energy": None,
    }

    def to_fr_date(us_date: str) -> str:
        dt = datetime.strptime(us_date, "%m/%d/%y")
        return dt.strftime("%d/%m/%Y")

    # Date d'émission
    m_due = re.search(
        r"Due\s+by[\s\n]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text, re.IGNORECASE
    )
    if m_due:
        data["date"] = to_fr_date(m_due.group(1))

    # Nom du destinataire
    m_recv = re.search(
        r"^([A-Z0-9 &\-\.'\,]+)\s*/\s*Page\b",
        text, re.MULTILINE
    )
    if m_recv:
        data["receiver_name"] = m_recv.group(1).strip()

    # Type d'énergie
    if re.search(r"\bgas\b", text, re.IGNORECASE):
        data["energy"] = "gas"
    elif re.search(r"\belectricity\b", text, re.IGNORECASE):
        data["energy"] = "electricity"

    return data
