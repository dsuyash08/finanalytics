"""
Download FY2021 & FY2022 annual report PDFs from BSE.

Reads data/annual_report_links.csv (company, fy, url) and saves each PDF to
reports/<COMPANY>_FY<YEAR>.pdf. BSE blocks requests without a browser-like
User-Agent and Referer, so those headers are set. Skips files already present.

Run:  py scripts/download_reports.py
"""

from __future__ import annotations

import csv
import os
import time
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINKS = os.path.join(BASE, "data", "annual_report_links.csv")
OUT = os.path.join(BASE, "reports")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Referer": "https://www.bseindia.com/",
    "Accept": "application/pdf,*/*",
}


def fetch(url: str, dest: str) -> tuple[bool, str]:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
    except Exception as e:  # noqa: BLE001
        return False, f"error: {e}"
    if len(data) < 1024 or not data[:5].startswith(b"%PDF"):
        return False, f"not a PDF ({len(data)} bytes)"
    with open(dest, "wb") as fh:
        fh.write(data)
    return True, f"{len(data)/1e6:.1f} MB"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    with open(LINKS, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    ok = 0
    for r in rows:
        company, fy, url = r["company"].strip(), r["fy"].strip(), r["url"].strip()
        if not url:
            continue
        dest = os.path.join(OUT, f"{company}_FY{fy}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest) > 1024:
            print(f"[have] {company} FY{fy}")
            ok += 1
            continue
        success, msg = fetch(url, dest)
        print(f"[{'ok' if success else 'FAIL'}] {company} FY{fy}: {msg}")
        ok += int(success)
        time.sleep(1.0)

    print(f"\n{ok}/{len(rows)} reports available in reports/")


if __name__ == "__main__":
    main()
