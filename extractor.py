#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil
import subprocess

NSIS_MAGIC = b"NullsoftInst"
CAB_MAGIC = b"MSCF"


def detectar_tipo_instalador(exe: Path) -> str | None:
    head = _leer_inicio(exe, 256_000)
    if head.startswith(CAB_MAGIC):
        return "cab"
    if NSIS_MAGIC in head:
        return "nsis"
    return None


def _herramientas_disponibles() -> tuple[str | None, str | None, str | None]:
    seven = (
        shutil.which("7z")
        or shutil.which("7zz")
        or shutil.which("7za")
        or shutil.which("7zr")
    )
    unrar = shutil.which("unrar") or shutil.which("rar")
    cab = shutil.which("cabextract")
    return seven, unrar, cab


def _leer_inicio(exe: Path, size: int) -> bytes:
    with exe.open("rb") as handle:
        return handle.read(size)


def extraer_actualizacion(
    exe_path: str = "Nacional_Sistema_1.7.0_update.exe",
    output_dir: str | None = None,
) -> str:
    """Extrae un instalador autoextraible (.exe) o un contenedor (.rar/.cab) en una carpeta.

    Requiere tener instalado alguno de: 7z / unrar / cabextract.

    Parametros:
        exe_path: Ruta al archivo .exe o .rar.
        output_dir: Carpeta destino (por defecto, nombre del archivo sin extension).
    Retorna:
        Ruta absoluta de la carpeta creada.
    """
    exe = Path(exe_path)
    if not exe.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {exe}")

    if output_dir is None:
        output_dir = exe.stem

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Detectar herramienta disponible
    seven, unrar, cab = _herramientas_disponibles()

    if seven:
        subprocess.run([seven, "x", str(exe), f"-o{out}", "-y"], check=True)
    elif unrar:
        subprocess.run([unrar, "x", "-y", str(exe), str(out)], check=True)
    elif cab and _leer_inicio(exe, 4).startswith(CAB_MAGIC):
        subprocess.run(["cabextract", "-d", str(out), str(exe)], check=True)
    else:
        tipo = detectar_tipo_instalador(exe)
        if tipo == "cab":
            raise RuntimeError(
                "No se encontro 7z/unrar. Para archivos CAB instala cabextract o 7zip."
            )
        if tipo == "nsis":
            raise RuntimeError(
                "No se encontro 7z/unrar. El instalador parece NSIS; instala 7zip (7z/7zz)."
            )
        raise RuntimeError("Instala 7zip (7z/7zz) o unrar para extraer este ejecutable.")

    return str(out.resolve())


def listar_contenido(exe_path: str = "Nacional_Sistema_1.7.0_update.exe") -> None:
    exe = Path(exe_path)
    if not exe.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {exe}")

    seven, unrar, cab = _herramientas_disponibles()
    if seven:
        subprocess.run([seven, "l", str(exe)], check=True)
        return
    if unrar:
        subprocess.run([unrar, "l", str(exe)], check=True)
        return
    if cab and _leer_inicio(exe, 4).startswith(CAB_MAGIC):
        subprocess.run(["cabextract", "-l", str(exe)], check=True)
        return

    tipo = detectar_tipo_instalador(exe)
    if tipo == "cab":
        raise RuntimeError("No se encontro 7z/unrar. Para CAB instala cabextract o 7zip.")
    if tipo == "nsis":
        raise RuntimeError(
            "No se encontro 7z/unrar. El instalador parece NSIS; instala 7zip (7z/7zz)."
        )
    raise RuntimeError("Instala 7zip (7z/7zz) o unrar para listar este ejecutable.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extrae o lista el contenido de Nacional_Sistema_1.7.0_update.exe "
            "usando 7zip/unrar/cabextract."
        )
    )
    parser.add_argument(
        "archivo",
        nargs="?",
        default="Nacional_Sistema_1.7.0_update.exe",
        help="Ruta al archivo .exe/.rar/.cab",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Carpeta destino (por defecto, nombre del archivo sin extension)",
    )
    parser.add_argument(
        "--listar",
        action="store_true",
        help="Solo listar contenido sin extraer",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    try:
        if args.listar:
            listar_contenido(args.archivo)
            return 0
        salida = extraer_actualizacion(args.archivo, args.output)
    except Exception as exc:
        print(f"Error: {exc}")
        return 1
    print(salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
