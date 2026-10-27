import requests
import time
import os
import calendar
import re
from pathlib import Path
from datetime import date
from dotenv import load_dotenv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

load_dotenv()
url = os.getenv("URL")

# Sin un User-Agent de navegador el sitio puede rechazar la petición
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

html = response.text
soup = BeautifulSoup(html, "html.parser")

# {"january": 1, ..., "december": 12}
MONTHS = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}

# Ej: "Lodgement data - January 2024" -> ("January", "2024")
PATTERN = re.compile(
    r"lodgement data\s*-\s*(" + "|".join(MONTHS) + r")\s+(\d{4})",
    re.IGNORECASE,
)

# Mapea cada mes (primer día) a la URL de su .xlsx
monthly = {}
for a in soup.find_all("a", href=True):
    href = a["href"]
    if not href.lower().endswith(".xlsx"):
        continue

    text = a.get_text(strip=True)
    match = PATTERN.search(text)
    if match is None:
        continue

    month = MONTHS[match.group(1).lower()]
    year = int(match.group(2))
    monthly[date(year, month, 1)] = urljoin(url, href)


START = date(2023, 1, 1)
END = date(2026, 9, 1)

selected = {d: link for d, link in monthly.items() if START <= d <= END}

print("Selected files:", len(selected))

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for d in sorted(selected):
    filename = f"lodgements_{d.year}_{d.month:02d}.xlsx"
    dest = OUTPUT_DIR / filename

    # Evita volver a descargar archivos existentes
    if dest.exists():
        print("Skip", filename)
        continue

    print("Downloading", filename)
    file_response = requests.get(selected[d], headers=headers, timeout=60)
    file_response.raise_for_status()
    dest.write_bytes(file_response.content)

    # Evita saturar el servidor
    time.sleep(1)
