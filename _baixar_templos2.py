"""Retry missing temple downloads via Commons Special:FilePath redirects."""
from __future__ import annotations

import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

OUT = Path("imagens")
UA = {"User-Agent": "WDD131StudentBot/1.0 (educational assignment)"}

# Use Special:FilePath so hashes/paths resolve correctly
TEMPLOS = [
    ("sao-paulo.jpg", "Sao Paulo Brazil Temple.jpg"),
    ("campinas.jpg", "Anjo Moroni no Templo Mórmon , Símbolo da Igreja. - panoramio.jpg"),
    ("recife.jpg", "Recife Brazile Temple by denalidog cropped.jpg"),
    ("porto-alegre.jpg", "Anjo Moroni Templo de Porto Alegre (20 January 2026).jpg"),
    ("manaus.jpg", "Templo SUD de Manaus 3.JPG"),
    ("fortaleza.jpg", "Fortaleza Brazil Temple behind.jpg"),
    ("curitiba.jpg", "Curitiba Brazil Temple 8091 by David Terry.jpeg"),
    ("manaus2.jpg", "Templo de Manaus de A Igreja de Jesus Cristo dos Santos dos Últimos Dias.jpg"),
]


def file_path_url(filename: str) -> str:
    from urllib.parse import quote
    return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width=1200"


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def optimize(data: bytes, dest: Path) -> int:
    img = Image.open(BytesIO(data)).convert("RGB")
    img.thumbnail((900, 900), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=65, optimize=True)
    return dest.stat().st_size


def main() -> None:
    for i, (arquivo, commons_name) in enumerate(TEMPLOS):
        dest = OUT / arquivo
        # re-download porto-alegre if tiny, and missing ones
        need = (not dest.exists()) or dest.stat().st_size < 20_000 or arquivo in {
            "campinas.jpg",
            "fortaleza.jpg",
            "manaus.jpg",
            "porto-alegre.jpg",
        }
        if not need:
            print("OK keep", arquivo, dest.stat().st_size)
            continue
        print("Baixando", arquivo, "<-", commons_name)
        try:
            raw = download(file_path_url(commons_name))
            size = optimize(raw, dest)
            print("  salvo", size)
        except Exception as exc:
            print("  erro", exc)
        time.sleep(6)


if __name__ == "__main__":
    main()
