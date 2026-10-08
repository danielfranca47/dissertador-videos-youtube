"""Captura os ecrãs relevantes de um vídeo já extraído por extrair_video.py
ou de uma gravação local já preparada por preparar_local.py.

Uso:
    python scripts/capturar_ecras.py <pasta-do-video>
    python scripts/capturar_ecras.py <pasta-do-video> --em 12:30,1:02:15
    python scripts/capturar_ecras.py <pasta-do-video> --limiar 0.15

Sem --em:
    1. Descarrega o vídeo (até 1080p, sem som) para <pasta>/video.mp4.
       Numa gravação local não descarrega nada: lê o ficheiro onde ele está.
    2. Deteta mudanças de ecrã com o ffmpeg e acrescenta capturas onde
       houver intervalos longos sem nenhuma (cobertura mínima).
    3. Extrai as imagens, descarta as quase iguais à anterior e grava em
       <pasta>/ecras/MM-SS.jpg, com o índice em <pasta>/ecras/indice.json.
    4. Monta folhas de miniaturas (<pasta>/ecras/folhas/) para rever
       rapidamente o que foi capturado.

Com --em: extrai só os instantes indicados (o vídeo tem de já estar descarregado).
Com --limiar: sensibilidade da deteção (padrão 0.08). Valores maiores (0.15-0.3)
    captam só as mudanças grandes de ecrã e geram menos imagens.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps
from yt_dlp import YoutubeDL

LIMIAR_CENA = 0.08          # sensibilidade da deteção de mudança de ecrã (0-1)
ATRASO_CAPTURA = 1.5        # segundos depois da mudança, para o ecrã assentar
INTERVALO_MAXIMO = 60       # se passar mais do que isto sem captura, acrescenta uma
DISTANCIA_MINIMA = 6        # bits de diferença (dhash 64 bits) para contar como ecrã novo
FOLHA_COLUNAS, FOLHA_LINHAS = 3, 3


def minuto(segundos: float) -> str:
    s = int(segundos)
    h, resto = divmod(s, 3600)
    m, s = divmod(resto, 60)
    return f"{h}-{m:02d}-{s:02d}" if h else f"{m:02d}-{s:02d}"


def segundos(texto: str) -> float:
    total = 0.0
    for parte in texto.strip().split(":"):
        total = total * 60 + float(parte)
    return total


def descarregar(link: str, destino: Path) -> None:
    if destino.exists():
        return
    opcoes = {
        "format": "bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]",
        "outtmpl": str(destino),
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(opcoes) as ydl:
        ydl.download([link])


def duracao(video: Path) -> float:
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(video)],
        capture_output=True, text=True, check=True).stdout
    return float(saida.strip())


def mudancas_de_ecra(video: Path, limiar: float) -> list[float]:
    filtro = f"scale=480:-1,select='gt(scene,{limiar})',showinfo"
    resultado = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(video), "-vf", filtro,
         "-an", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [float(t) for t in re.findall(r"pts_time:([\d.]+)", resultado.stderr)]


def instantes_candidatos(mudancas: list[float], total: float) -> list[float]:
    # Arredonda ao segundo: o nome do arquivo é MM-SS, e dois instantes no mesmo
    # segundo gravariam por cima um do outro.
    instantes = sorted({float(int(min(t + ATRASO_CAPTURA, total - 1))) for t in mudancas} | {5.0})
    completos, anterior = [], 0.0
    for t in instantes + [total - 1]:
        while t - anterior > INTERVALO_MAXIMO:
            anterior += INTERVALO_MAXIMO
            completos.append(anterior)
        completos.append(t)
        anterior = t
    return sorted(set(completos))


def extrair(video: Path, t: float, destino: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.2f}",
         "-i", str(video), "-frames:v", "1", "-q:v", "3", str(destino)],
        check=True)


def dhash(caminho: Path) -> int:
    img = Image.open(caminho).convert("L").resize((9, 8))
    px = list(img.getdata())
    bits = 0
    for linha in range(8):
        for col in range(8):
            bits = (bits << 1) | (px[linha * 9 + col] > px[linha * 9 + col + 1])
    return bits


def montar_folhas(imagens: list[Path], pasta: Path) -> None:
    pasta.mkdir(exist_ok=True)
    por_folha = FOLHA_COLUNAS * FOLHA_LINHAS
    largura, altura = 640, 346
    for n in range(0, len(imagens), por_folha):
        grupo = imagens[n:n + por_folha]
        folha = Image.new("RGB", (largura * FOLHA_COLUNAS, (altura + 24) * FOLHA_LINHAS), "white")
        desenho = ImageDraw.Draw(folha)
        for i, caminho in enumerate(grupo):
            x, y = (i % FOLHA_COLUNAS) * largura, (i // FOLHA_COLUNAS) * (altura + 24)
            # Mantém a proporção: um clipe de telemóvel ao alto não fica esticado.
            miniatura = ImageOps.contain(Image.open(caminho), (largura, altura))
            folha.paste(miniatura, (x + (largura - miniatura.width) // 2, y + 24))
            desenho.text((x + 6, y + 5), caminho.stem, fill="black")
        folha.save(pasta / f"folha-{n // por_folha + 1:02d}.jpg", quality=80)


def main() -> int:
    argumentos = sys.argv[1:]
    if not argumentos:
        print(__doc__)
        return 1
    pasta = Path(argumentos[0]).resolve()
    metadados = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    # Uma gravação local é lida onde está, e os ecrãs dela só podem ir para fora do git.
    local = metadados.get("ficheiro")
    if local:
        from preparar_local import exigir_fora_do_git
        exigir_fora_do_git(pasta)
    video = Path(local) if local else pasta / "video.mp4"
    ecras = pasta / "ecras"
    ecras.mkdir(exist_ok=True)

    if "--em" in argumentos:
        for texto in argumentos[argumentos.index("--em") + 1].split(","):
            t = segundos(texto)
            destino = ecras / f"{minuto(t)}.jpg"
            extrair(video, t, destino)
            print(destino)
        return 0

    for antigo in ecras.glob("*.jpg"):
        antigo.unlink()

    if not local:
        print("A descarregar o vídeo...")
        descarregar(metadados["link"], video)
    total = duracao(video)
    print("A detetar mudanças de ecrã...")
    limiar = float(argumentos[argumentos.index("--limiar") + 1]) if "--limiar" in argumentos else LIMIAR_CENA
    mudancas = mudancas_de_ecra(video, limiar)
    candidatos = instantes_candidatos(mudancas, total)
    print(f"{len(mudancas)} mudanças detetadas, {len(candidatos)} instantes candidatos")

    guardadas, ultimo_hash = [], None
    for t in candidatos:
        destino = ecras / f"{minuto(t)}.jpg"
        extrair(video, t, destino)
        h = dhash(destino)
        if ultimo_hash is not None and bin(h ^ ultimo_hash).count("1") < DISTANCIA_MINIMA:
            destino.unlink()
            continue
        ultimo_hash = h
        guardadas.append({"instante": minuto(t).replace("-", ":"), "segundos": round(t, 1),
                          "arquivo": destino.name,
                          "origem": "mudança de ecrã" if any(0 <= t - m < ATRASO_CAPTURA + 1 for m in mudancas) else "cobertura"})

    (ecras / "indice.json").write_text(json.dumps(guardadas, ensure_ascii=False, indent=2), encoding="utf-8")
    montar_folhas([ecras / g["arquivo"] for g in guardadas], ecras / "folhas")
    print(f"{len(guardadas)} ecrãs guardados em {ecras}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
