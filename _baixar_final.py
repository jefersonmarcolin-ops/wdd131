"""Download final set of 9 operating Brazil LDS temple photos."""
from __future__ import annotations

import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

OUT = Path("imagens")
UA = {"User-Agent": "WDD131StudentBot/1.0 (educational)"}

TEMPLOS = [
    ("sao-paulo.jpg", "Templo de sao paulo.jpg", "Templo de São Paulo Brasil", "templo antigo grande"),
    ("campinas.jpg", "Campinas Brazil Temple by Andres Segal.jpeg", "Templo de Campinas Brasil", "templo antigo grande"),
    ("recife.jpg", "Templo do Recife, (Recife - PE, Brasil).jpg", "Templo de Recife Brasil", "templo antigo pequeno"),
    ("porto-alegre.jpg", "Templo de Porto Alegre (20 January 2026).jpg", "Templo de Porto Alegre Brasil", "templo antigo pequeno"),
    ("manaus.jpg", "Templo de Manaus.jpg", "Templo de Manaus Brasil", "templo antigo pequeno"),
    ("fortaleza.jpg", "Fortaleza Brazil Temple.jpg", "Templo de Fortaleza Brasil", "templo novo grande"),
    ("curitiba.jpg", "TemploMormonCuritiba.JPG", "Templo de Curitiba Brasil", "templo antigo grande"),
    ("sao-paulo-2.jpg", "Sao Paulo Brazil Temple.jpg", "Templo de São Paulo Brasil (vista 2)", "templo antigo grande"),
    # Prefer a second fortaleza/curitiba/manaus if Rio/Belem unavailable
    ("manaus-2.jpg", "Templo SUD de Manaus 3.JPG", "Templo de Manaus Brasil (vista 2)", "templo antigo pequeno"),
]


def filepath(name: str) -> str:
    return (
        "https://commons.wikimedia.org/wiki/Special:FilePath/"
        + urllib.parse.quote(name)
        + "?width=1200"
    )


def download_optimize(commons_name: str, dest: Path) -> int:
    url = filepath(commons_name)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as resp:
        raw = resp.read()
    img = Image.open(BytesIO(raw)).convert("RGB")
    img.thumbnail((900, 900), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=68, optimize=True)
    return dest.stat().st_size


def main() -> None:
    ok = []
    for arquivo, commons, nome, classes in TEMPLOS:
        dest = OUT / arquivo
        print("Baixando", nome)
        try:
            size = download_optimize(commons, dest)
            print("  OK", arquivo, size)
            ok.append((arquivo, nome, classes, size))
        except Exception as exc:
            print("  FALHOU", exc)
        time.sleep(5)
    print("\nSucesso:", len(ok))
    for row in ok:
        print(row)


if __name__ == "__main__":
    main()
