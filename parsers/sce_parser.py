import re
from datetime import datetime

def parse_sce(text: str) -> dict:
    """
    Extrait des factures Southern California Edison :
      • supplier (fixe)
      • date d'émission (après 'Due by')
      • receiver_name : nom du destinataire (ligne avant '/ Page')
    """
    data = {
        "supplier": "SouthernCaliforniaEdison",
        "date": None,
        "receiver_name": None,
    }

    def to_fr_date(us_date: str) -> str:
        # attend MM/DD/YY ou MM/DD/YYYY
        dt = datetime.strptime(us_date, "%m/%d/%y")
        return dt.strftime("%d/%m/%Y")

    # 1) Date d'émission : on cherche la première occurrence de "Due by" + date
    m_due = re.search(
        r"Due\s+by[\s\n]*([0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4})",
        text,
        re.IGNORECASE
    )
    if m_due:
        data["date"] = to_fr_date(m_due.group(1))

    # 2) Nom du destinataire (ligne avant "/ Page")
    m_recv = re.search(
        r"^([A-Z0-9 &\-\.'\,]+)\s*/\s*Page\b",
        text,
        re.MULTILINE
    )
    if m_recv:
        data["receiver_name"] = m_recv.group(1).strip()

    return data
