"""List and download better-identified Brazil temple photos from Commons."""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

OUT = Path("imagens")
UA = {"User-Agent": "WDD131StudentBot/1.0 (educational)"}


def get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)


def category_files(cat: str, limit: int = 10) -> list[tuple[str, str]]:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "generator": "categorymembers",
            "gcmtype": "file",
            "gcmtitle": f"Category:{cat}",
            "gcmlimit": limit,
            "prop": "imageinfo",
            "iiprop": "url|size|mime",
        }
    )
    data = get_json(url)
    pages = data.get("query", {}).get("pages", {})
    out = []
    for p in pages.values():
        title = p.get("title", "").replace("File:", "")
        info = (p.get("imageinfo") or [{}])[0]
        if str(info.get("mime", "")).startswith("image/"):
            out.append((title, info.get("url") or ""))
    return out


def download_optimize(url: str, dest: Path) -> int:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    img = Image.open(BytesIO(raw)).convert("RGB")
    img.thumbnail((900, 900), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=68, optimize=True)
    return dest.stat().st_size


def filepath(name: str) -> str:
    return (
        "https://commons.wikimedia.org/wiki/Special:FilePath/"
        + urllib.parse.quote(name)
        + "?width=1200"
    )


# Curated picks: filename -> output jpg
PICKS = {
    "sao-paulo.jpg": "Templo de sao paulo.jpg",
    "campinas.jpg": "Campinas Brazil Temple.jpg",  # may fail
    "recife.jpg": "Recife Brazile Temple by denalidog - Alan.jpg",
    "manaus.jpg": "Templo SUD de Manaus 3.JPG",
    "fortaleza.jpg": "Fortaleza Brazil Temple behind.jpg",
    "curitiba.jpg": "Curitiba Brazil Temple 8091 by David Terry.jpeg",
}

CATEGORIES = [
    "São Paulo Brazil Temple",
    "Campinas Brazil Temple",
    "Recife Brazil Temple",
    "Porto Alegre Brazil Temple",
    "Manaus Brazil Temple",
    "Fortaleza Brazil Temple",
    "Curitiba Brazil Temple",
]


def main() -> None:
    print("=== Listing categories ===")
    for cat in CATEGORIES:
        try:
            files = category_files(cat)
            print(cat, len(files))
            for title, url in files[:6]:
                print(" -", title)
        except Exception as exc:
            print(cat, "ERR", exc)
        time.sleep(3)

    print("\n=== Downloading curated ===")
    for dest_name, commons_name in PICKS.items():
        dest = OUT / dest_name
        print("Get", dest_name, "<-", commons_name)
        try:
            size = download_optimize(filepath(commons_name), dest)
            print("  OK", size)
        except Exception as exc:
            print("  fail", exc)
        time.sleep(5)


if __name__ == "__main__":
    main()
