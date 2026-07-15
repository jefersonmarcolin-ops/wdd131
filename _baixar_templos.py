"""Download Brazil LDS temple photos with delays to avoid 429."""
from __future__ import annotations

import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

OUT = Path("imagens")
UA = {"User-Agent": "WDD131StudentBot/1.0 (educational; contact: student assignment)"}

# Direct upload.wikimedia.org URLs (or known good paths)
TEMPLOS = [
    {
        "arquivo": "sao-paulo.jpg",
        "nome": "Templo de São Paulo Brasil",
        "classes": "templo antigo grande",
        "url": "https://upload.wikimedia.org/wikipedia/commons/c/c4/Sao_Paulo_Brazil_Temple.jpg",
    },
    {
        "arquivo": "campinas.jpg",
        "nome": "Templo de Campinas Brasil",
        "classes": "templo antigo grande",
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/57/A_linda_Igreja_vista_pela_Decathlon_-_panoramio.jpg",
    },
    {
        "arquivo": "recife.jpg",
        "nome": "Templo de Recife Brasil",
        "classes": "templo antigo pequeno",
        "url": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Recife_Brazile_Temple_by_denalidog_cropped.jpg",
    },
    {
        "arquivo": "porto-alegre.jpg",
        "nome": "Templo de Porto Alegre Brasil",
        "classes": "templo antigo pequeno",
        "url": "https://upload.wikimedia.org/wikipedia/commons/0/06/Anjo_Moroni_Templo_de_Porto_Alegre_%2820_January_2026%29.jpg",
    },
    {
        "arquivo": "manaus.jpg",
        "nome": "Templo de Manaus Brasil",
        "classes": "templo antigo pequeno",
        "url": "https://upload.wikimedia.org/wikipedia/commons/7/76/Templo_de_Manaus_de_A_Igreja_de_Jesus_Cristo_dos_Santos_dos_%C3%9Altimos_Dias.jpg",
    },
    {
        "arquivo": "fortaleza.jpg",
        "nome": "Templo de Fortaleza Brasil",
        "classes": "templo novo grande",
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/64/Fortaleza_Brazil_Temple_behind.jpg",
    },
    {
        "arquivo": "curitiba.jpg",
        "nome": "Templo de Curitiba Brasil",
        "classes": "templo antigo grande",
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Curitiba_Brazil_Temple_8091_by_David_Terry.jpeg",
    },
]


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
    ok = []
    for i, item in enumerate(TEMPLOS):
        dest = OUT / item["arquivo"]
        if dest.exists() and dest.stat().st_size > 10_000:
            print("Ja existe:", item["arquivo"], dest.stat().st_size)
            ok.append(item)
            continue
        print("Baixando:", item["nome"])
        try:
            raw = download(item["url"])
            size = optimize(raw, dest)
            print("  OK", size, "bytes")
            ok.append(item)
        except Exception as exc:
            print("  ERRO:", exc)
        if i < len(TEMPLOS) - 1:
            time.sleep(4)
    print("Concluidos:", len(ok))


if __name__ == "__main__":
    main()
