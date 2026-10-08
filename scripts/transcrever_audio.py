"""Transcreve na própria máquina a fala de uma gravação local já preparada.

Uso:
    python scripts/transcrever_audio.py --descarregar-modelo
    python scripts/transcrever_audio.py <pasta-do-video>
    python scripts/transcrever_audio.py <pasta-do-video> --vocabulario "e-Fatura, OfficeGest, NIF"
    python scripts/transcrever_audio.py <pasta-do-video> --trecho 33:00-43:00 --saida transcricao-trecho.txt
    python scripts/transcrever_audio.py <pasta-do-video> --modelo small --threads 4

Grava <pasta>/transcricao.txt no mesmo formato das legendas do YouTube: blocos
de ~30 s com o minuto de início. No fim diz quanto tempo demorou, quanto do
vídeo é fala e se encontrou frases repetidas (sinal de texto inventado).

O som nunca sai da máquina. A transcrição corre com a rede desligada para a
biblioteca; só --descarregar-modelo vai à internet, uma vez, buscar o modelo
(~1,6 GB). Sem placa gráfica, conte com cerca de 1 a 1,5 vezes a duração do
áudio, com o computador mais lento enquanto corre.

--vocabulario  termos do assunto, para o modelo os escrever bem
--trecho       transcreve só esse intervalo (os minutos continuam a ser os do vídeo)
--saida        nome do ficheiro de texto (padrão: transcricao.txt)
--modelo       padrão large-v3-turbo; "small" é mais rápido e erra mais
--threads      núcleos a usar (padrão: metade dos que a máquina mostra)
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from capturar_ecras import segundos
from extrair_video import agrupar, minuto
from preparar_local import exigir_fora_do_git, opcao

MODELO = "large-v3-turbo"
IDIOMA = "pt"
AMOSTRAS_POR_SEGUNDO = 16000
REPETICOES_SUSPEITAS = 3    # a mesma frase tantas vezes seguidas conta como texto inventado
AVISO_A_CADA = 300          # segundos de áudio entre cada linha de progresso


def ler_som(video: Path, inicio: float, fim: float | None) -> np.ndarray:
    comando = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{inicio:.2f}", "-i", str(video)]
    if fim is not None:
        comando += ["-t", f"{fim - inicio:.2f}"]
    comando += ["-vn", "-ac", "1", "-ar", str(AMOSTRAS_POR_SEGUNDO), "-f", "s16le", "-"]
    bruto = subprocess.run(comando, capture_output=True, check=True).stdout
    return np.frombuffer(bruto, np.int16).astype(np.float32) / 32768.0


def repeticoes(textos: list[str]) -> int:
    """Quantas vezes a mesma frase aparece REPETICOES_SUSPEITAS vezes seguidas."""
    total, seguidas = 0, 1
    for anterior, atual in zip(textos, textos[1:]):
        seguidas = seguidas + 1 if atual == anterior else 1
        if seguidas == REPETICOES_SUSPEITAS:
            total += 1
    return total


def gravar(destino: Path, trechos: list[tuple[float, str]]) -> int:
    blocos = agrupar(trechos)
    destino.write_text("\n\n".join(blocos) + "\n", encoding="utf-8")
    return len(blocos)


def main() -> int:
    argumentos = sys.argv[1:]
    if not argumentos:
        print(__doc__)
        return 1
    modelo = opcao(argumentos, "--modelo", MODELO)

    if argumentos[0] == "--descarregar-modelo":
        from faster_whisper import download_model
        print(f"Modelo {modelo} em {download_model(modelo)}")
        return 0

    # Daqui em diante a biblioteca não pode ir à internet: tem de ser definido
    # antes de a importar.
    os.environ["HF_HUB_OFFLINE"] = "1"
    from faster_whisper import WhisperModel

    pasta = Path(argumentos[0]).resolve()
    metadados = json.loads((pasta / "metadados.json").read_text(encoding="utf-8"))
    if metadados.get("origem") != "local":
        print("Só gravações locais (preparar_local.py). Vídeos do YouTube sem legendas ainda não são transcritos.")
        return 1
    if not metadados.get("tem_som"):
        print("O vídeo não tem som.")
        return 2
    exigir_fora_do_git(pasta)

    trecho = opcao(argumentos, "--trecho")
    inicio, fim = (segundos(t) for t in trecho.split("-")) if trecho else (0.0, None)
    vocabulario = opcao(argumentos, "--vocabulario")
    threads = int(opcao(argumentos, "--threads", (os.cpu_count() or 2) // 2))
    destino = pasta / opcao(argumentos, "--saida", "transcricao.txt")

    try:
        motor = WhisperModel(modelo, device="cpu", compute_type="int8",
                             cpu_threads=threads, local_files_only=True)
    except Exception as erro:
        print(f"O modelo {modelo} não está na máquina ({type(erro).__name__}).\n"
              f"Corra primeiro: python scripts/transcrever_audio.py --descarregar-modelo --modelo {modelo}")
        return 2

    print("A ler o som do vídeo...")
    som = ler_som(Path(metadados["ficheiro"]), inicio, fim)
    duracao = len(som) / AMOSTRAS_POR_SEGUNDO
    if duracao < 1:
        print(f"Não há som nesse intervalo. A faixa de som deste vídeo acaba aos "
              f"{minuto(metadados.get('segundos_de_som', 0))}.")
        return 2
    print(f"A transcrever {minuto(duracao)} de áudio com o modelo {modelo} ({threads} núcleos)...")

    arranque = time.monotonic()
    # Não condicionar no texto anterior: evita que uma frase inventada num
    # silêncio se repita pelos blocos seguintes.
    partes, info = motor.transcribe(som, language=IDIOMA, vad_filter=True,
                                    condition_on_previous_text=False, hotwords=vocabulario)
    trechos, proximo_aviso = [], AVISO_A_CADA
    for parte in partes:
        texto = " ".join(parte.text.split())
        if texto:
            trechos.append((inicio + parte.start, texto))
        if parte.end >= proximo_aviso:
            gravar(destino, trechos)
            print(f"  {minuto(inicio + parte.end)} transcrito, {minuto(time.monotonic() - arranque)} decorridos", flush=True)
            proximo_aviso += AVISO_A_CADA
    demorou = time.monotonic() - arranque

    blocos = gravar(destino, trechos)
    repetidas = repeticoes([texto for _, texto in trechos])
    medicao = {
        "origem": "transcrição local do áudio",
        "motor": "faster-whisper",
        "modelo": modelo,
        "idioma": IDIOMA,
        "vocabulario": vocabulario,
        "trecho": trecho,
        "segundos_de_audio": round(duracao, 1),
        "segundos_de_fala": round(info.duration_after_vad, 1),
        "segundos_de_processamento": round(demorou, 1),
        "frases_repetidas": repetidas,
    }
    if destino.name == "transcricao.txt":
        metadados["legenda"] = medicao
        (pasta / "metadados.json").write_text(
            json.dumps(metadados, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Texto: {destino} ({blocos} blocos)")
    print(f"Demorou {minuto(demorou)} para {minuto(duracao)} de áudio: {demorou / duracao:.2f} vezes a duração")
    print(f"Fala: {minuto(info.duration_after_vad)} ({100 * info.duration_after_vad / duracao:.0f}% do áudio)")
    print(f"Frases repetidas {REPETICOES_SUSPEITAS} vezes seguidas: {repetidas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
