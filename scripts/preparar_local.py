"""Prepara uma gravação local (um ficheiro de vídeo no disco) para ser analisada.

Uso:
    python scripts/preparar_local.py <ficheiro-de-video> --destino <pasta>
    python scripts/preparar_local.py <ficheiro-de-video> --destino <pasta> --titulo "<título>" --gravado AAAA-MM-DD

Cria <pasta>/metadados.json com o caminho do ficheiro, a duração, a resolução
e se tem som. O vídeo é lido onde está: não é copiado nem alterado.

É o primeiro passo para gravações com dados reais, que não podem passar pelo
YouTube. Por isso a pasta de destino tem de estar fora do git: ou fora de
qualquer repositório, ou numa pasta que o repositório ignora. Se não estiver,
o script recusa e termina com o código de saída 3.

Depois deste passo: transcrever_audio.py (a fala) e capturar_ecras.py (os ecrãs).
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from extrair_video import minuto

SOM_EM_FALTA = 5    # segundos de imagem sem som, no fim, a partir dos quais se avisa


def opcao(argumentos: list[str], nome: str, padrao=None):
    return argumentos[argumentos.index(nome) + 1] if nome in argumentos else padrao


def fora_do_git(pasta: Path) -> bool:
    """True se nada do que for gravado em `pasta` pode entrar num repositório."""
    existente = pasta
    while not existente.exists():
        existente = existente.parent
    dentro = subprocess.run(
        ["git", "-C", str(existente), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True)
    if dentro.returncode != 0 or dentro.stdout.strip() != "true":
        return True
    ignorada = subprocess.run(
        ["git", "-C", str(existente), "check-ignore", "-q", str(pasta)],
        capture_output=True)
    return ignorada.returncode == 0


def exigir_fora_do_git(pasta: Path) -> None:
    if not fora_do_git(pasta):
        print(f"Recusado: {pasta} está dentro de um repositório git e não é ignorada.\n"
              "Uma gravação local pode ter dados reais; escolha uma pasta fora do git.")
        sys.exit(3)


def ler_video(ficheiro: Path) -> dict:
    saida = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height,duration:stream_side_data=rotation",
         "-of", "json", str(ficheiro)],
        capture_output=True, text=True, encoding="utf-8", check=True).stdout
    dados = json.loads(saida)
    imagem = next((s for s in dados["streams"] if s.get("codec_type") == "video"), {})
    som = next((s for s in dados["streams"] if s.get("codec_type") == "audio"), None)
    largura, altura = imagem.get("width"), imagem.get("height")
    rodado = any(abs(int(d.get("rotation", 0))) in (90, 270) for d in imagem.get("side_data_list", []))
    if rodado:
        largura, altura = altura, largura
    segundos = round(float(dados["format"]["duration"]), 1)
    return {
        "segundos": segundos,
        "resolucao": f"{largura}x{altura}" if largura else None,
        "tem_som": som is not None,
        # A faixa de som pode acabar antes da imagem (a gravação perdeu o som a meio).
        "segundos_de_som": round(float(som.get("duration") or segundos), 1) if som else 0.0,
    }


def main() -> int:
    argumentos = sys.argv[1:]
    if len(argumentos) < 3 or "--destino" not in argumentos:
        print(__doc__)
        return 1
    ficheiro = Path(argumentos[0]).resolve()
    pasta = Path(opcao(argumentos, "--destino")).resolve()
    if not ficheiro.is_file():
        print(f"Ficheiro não encontrado: {ficheiro}")
        return 1
    exigir_fora_do_git(pasta)

    video = ler_video(ficheiro)
    gravado = opcao(argumentos, "--gravado") or datetime.fromtimestamp(ficheiro.stat().st_mtime).strftime("%Y-%m-%d")
    # Preparar de novo uma pasta já transcrita não apaga o registo da transcrição.
    existente = pasta / "metadados.json"
    anterior = json.loads(existente.read_text(encoding="utf-8")) if existente.exists() else {}
    metadados = {
        "origem": "local",
        "ficheiro": str(ficheiro),
        "id": pasta.name,
        "titulo": opcao(argumentos, "--titulo") or ficheiro.stem,
        "gravado": gravado,
        "duracao": minuto(video["segundos"]),
        "segundos": video["segundos"],
        "resolucao": video["resolucao"],
        "tem_som": video["tem_som"],
        "segundos_de_som": video["segundos_de_som"],
        "legenda": anterior.get("legenda"),
    }
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "metadados.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Pasta: {pasta}")
    print(f"Título: {metadados['titulo']} ({metadados['duracao']}, {gravado}, {video['resolucao']})")
    if not video["tem_som"]:
        print("Som: não tem. Não há fala para transcrever.")
    elif video["segundos"] - video["segundos_de_som"] > SOM_EM_FALTA:
        print(f"Som: ATENÇÃO, só existe até {minuto(video['segundos_de_som'])}. "
              f"O resto do vídeo (até {metadados['duracao']}) não tem som.")
    else:
        print("Som: sim")
    return 0


if __name__ == "__main__":
    sys.exit(main())
