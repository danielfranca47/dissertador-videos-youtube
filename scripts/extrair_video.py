"""Extrai metadados e transcrição de um vídeo do YouTube.

Uso:
    python scripts/extrair_video.py <link-do-youtube> --tema <assunto>

Cria a pasta videos/<assunto>/<titulo-do-video>/ com:
    metadados.json   título, canal, data de publicação, duração, descrição, capítulos
    transcricao.txt  fala do vídeo em blocos de ~30 s, com o minuto de início

A transcrição vem das legendas do YouTube (manuais primeiro, depois automáticas).
Se o vídeo não tiver legendas, o script avisa e termina: a transcrição do áudio
fica para uma fase seguinte.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.request import urlopen

from yt_dlp import YoutubeDL

RAIZ = Path(__file__).resolve().parent.parent
BLOCO_SEGUNDOS = 30
IDIOMAS_PREFERIDOS = ["pt-PT", "pt", "pt-BR", "en"]


def nome_de_pasta(texto: str) -> str:
    """'Webinar #2: Contabilidade OfficeGest' -> 'webinar-2-contabilidade-officegest'."""
    sem_acentos = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sem_acentos.lower()).strip("-")[:60].rstrip("-") or "video"


def pasta_do_video(tema: str, info: dict) -> Path:
    """Pasta pelo assunto e título. Se outro vídeo já tiver o mesmo título, acrescenta o id."""
    pasta = RAIZ / "videos" / nome_de_pasta(tema) / nome_de_pasta(info.get("title") or info["id"])
    existente = pasta / "metadados.json"
    if existente.exists() and json.loads(existente.read_text(encoding="utf-8")).get("id") != info["id"]:
        pasta = pasta.with_name(f"{pasta.name}-{info['id']}")
    return pasta


def minuto(segundos: float) -> str:
    s = int(segundos)
    h, resto = divmod(s, 3600)
    m, s = divmod(resto, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def escolher_legenda(info: dict):
    """Devolve (origem, idioma, url json3) da melhor legenda disponível."""
    idioma_video = info.get("language") or ""
    candidatos = [f"{idioma_video}-orig", idioma_video] + IDIOMAS_PREFERIDOS
    for origem, faixas in (("manual", info.get("subtitles") or {}),
                           ("automática", info.get("automatic_captions") or {})):
        for idioma in candidatos:
            for formato in faixas.get(idioma, []):
                if formato.get("ext") == "json3":
                    return origem, idioma, formato["url"]
    return None


def ler_json3(url: str) -> list[tuple[float, str]]:
    with urlopen(url) as resposta:
        dados = json.load(resposta)
    trechos = []
    for evento in dados.get("events", []):
        texto = "".join(seg.get("utf8", "") for seg in evento.get("segs") or [])
        texto = " ".join(texto.split())
        if texto:
            trechos.append((evento.get("tStartMs", 0) / 1000, texto))
    return trechos


def agrupar(trechos: list[tuple[float, str]]) -> list[str]:
    blocos, inicio, partes = [], None, []
    for t, texto in trechos:
        if inicio is None:
            inicio = t
        elif t - inicio >= BLOCO_SEGUNDOS:
            blocos.append(f"[{minuto(inicio)}] " + " ".join(partes))
            inicio, partes = t, []
        partes.append(texto)
    if partes:
        blocos.append(f"[{minuto(inicio)}] " + " ".join(partes))
    return blocos


def main() -> int:
    argumentos = sys.argv[1:]
    if len(argumentos) != 3 or argumentos[1] != "--tema":
        print(__doc__)
        return 1
    link, tema = argumentos[0], argumentos[2]

    with YoutubeDL({"quiet": True, "skip_download": True, "no_warnings": True}) as ydl:
        info = ydl.extract_info(link, download=False)

    data = info.get("upload_date") or "00000000"
    pasta = pasta_do_video(tema, info)
    pasta.mkdir(parents=True, exist_ok=True)

    legenda = escolher_legenda(info)
    metadados = {
        "link": info.get("webpage_url"),
        "id": info["id"],
        "tema": tema,
        "titulo": info.get("title"),
        "canal": info.get("channel") or info.get("uploader"),
        "data_publicacao": f"{data[:4]}-{data[4:6]}-{data[6:]}",
        "duracao": info.get("duration_string"),
        "idioma": info.get("language"),
        "descricao": info.get("description"),
        "capitulos": [{"inicio": minuto(c["start_time"]), "titulo": c["title"]}
                      for c in info.get("chapters") or []],
        "legenda": {"origem": legenda[0], "idioma": legenda[1]} if legenda else None,
    }
    (pasta / "metadados.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")

    if not legenda:
        print(f"Sem legendas disponíveis. Metadados gravados em {pasta}")
        return 2

    blocos = agrupar(ler_json3(legenda[2]))
    (pasta / "transcricao.txt").write_text("\n\n".join(blocos) + "\n", encoding="utf-8")

    print(f"Pasta: {pasta}")
    print(f"Título: {metadados['titulo']} ({metadados['duracao']}, {metadados['data_publicacao']})")
    print(f"Legenda {legenda[0]} [{legenda[1]}]: {len(blocos)} blocos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
