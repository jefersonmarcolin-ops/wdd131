import re
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (compatible; WDD131Student/1.0; educational)"}
OUT = Path("imagens")


def save_image(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    img = Image.open(BytesIO(raw)).convert("RGB")
    img.thumbnail((900, 900), Image.Resampling.LANCZOS)
    img.save(dest, "JPEG", quality=68, optimize=True)
    print("saved", dest.name, dest.stat().st_size)


def extract_from_page(page_url: str) -> list[str]:
    req = urllib.request.Request(page_url, headers=UA)
    html = urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")
    patterns = [
        r'(https://churchofjesuschristtemples\.org/[^\"\'\s]+?\.(?:jpg|jpeg|png|webp))',
        r'(https://[^\"\'\s]*temples[^\"\'\s]+\.(?:jpg|jpeg|png|webp))',
        r'content=\"(https://[^\"\']+\.(?:jpg|jpeg|png|webp))\"',
    ]
    found: list[str] = []
    for pat in patterns:
        for u in re.findall(pat, html, flags=re.I):
            if u not in found and "logo" not in u.lower():
                found.append(u)
    return found


pages = {
    "rio-de-janeiro.jpg": "https://churchofjesuschristtemples.org/rio-de-janeiro-brazil-temple/",
    "belem.jpg": "https://churchofjesuschristtemples.org/belem-brazil-temple/",
}

for dest_name, page in pages.items():
    print("page", page)
    try:
        urls = extract_from_page(page)
        print(" found", len(urls))
        for u in urls[:5]:
            print(" ", u)
        dest = OUT / dest_name
        for u in urls:
            try:
                save_image(u, dest)
                break
            except Exception as exc:
                print("  skip", exc)
    except Exception as exc:
        print(" page fail", exc)
    time.sleep(2)
