from pathlib import Path
import subprocess
import sys
import shutil
import logging
from typing import List, Tuple
from dataclasses import dataclass
from itertools import chain

# Configuração de logging estruturado
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


@dataclass(frozen=True, slots=True)
class BuildConfig:
    main_py: Path
    assets_dir: Path
    hidden_imports: Tuple[str, ...]
    dist_dir: Path
    build_dir: Path
    exe_name: str = "trabalho-final"


def validate_paths(required: List[Tuple[Path, str]]) -> None:
    """Valida a existência dos arquivos e diretórios essenciais do projeto."""
    missing = [desc for path, desc in required if not path.exists()]
    if missing:
        logging.error("Arquivos/diretórios ausentes: %s", ", ".join(missing))
        raise FileNotFoundError(f"Arquivos/diretórios ausentes: {', '.join(missing)}")


def is_pyinstaller_installed() -> bool:
    """Verifica se o PyInstaller está instalado no ambiente atual."""
    try:
        subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            check=True,
            capture_output=True,
        )
        return True
    except Exception:
        return False


def clean_previous_builds(dist_dir: Path, build_dir: Path) -> None:
    """Remove diretórios de build anteriores para evitar resíduos."""
    for d in (dist_dir, build_dir):
        if d.exists():
            shutil.rmtree(d)
            logging.info("Diretório removido: %s", d)


def discover_image_files(assets_dir: Path) -> List[Path]:
    """
    Função pura. Descobre recursivamente todos os arquivos .png e .jpg em assets_dir.
    Retorna lista imutável de Paths.
    """
    return list(chain(assets_dir.rglob("*.png"), assets_dir.rglob("*.jpg")))


def build_pyinstaller_command(config: BuildConfig) -> list[str]:
    sep = ";" if sys.platform == "win32" else ":"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--name",
        config.exe_name,
        "--distpath",
        str(config.dist_dir),
        "--workpath",
        str(config.build_dir),
    ]
    for module in config.hidden_imports:
        cmd.extend(["--hidden-import", module])
    # Empacota cada imagem de src/assets para assets/
    for img in discover_image_files(config.assets_dir):
        rel_path = img.relative_to(config.assets_dir)
        dest_path = f"assets/{rel_path.as_posix()}"
        cmd.append(f"--add-data={img}{sep}{dest_path}")
    cmd.append(str(config.main_py))
    return cmd


def run_build(cmd: List[str]) -> None:
    """Executa o comando do PyInstaller e trata possíveis erros."""
    logging.info("Executando: %s", " ".join(str(arg) for arg in cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logging.error("Erro ao executar build: %s", e)
        raise RuntimeError(f"Erro ao executar build: {e}") from e
    except FileNotFoundError:
        logging.error(
            "PyInstaller não encontrado. Instale com: pip install pyinstaller"
        )
        raise RuntimeError(
            "PyInstaller não encontrado. Instale com: pip install pyinstaller"
        )


def validate_build_result(dist_dir: Path, exe_name: str) -> None:
    """Valida se o executável foi gerado corretamente."""
    exe_path = dist_dir / (exe_name + (".exe" if sys.platform == "win32" else ""))
    if not exe_path.exists() or exe_path.stat().st_size < 1024 * 100:
        logging.error(
            "Build falhou: executável não encontrado ou muito pequeno (%s)", exe_path
        )
        raise RuntimeError(
            f"Build falhou: executável não encontrado ou muito pequeno ({exe_path})"
        )
    logging.info("✅ Build concluído! Executável em: %s", exe_path)


def build() -> None:
    """
    Gera o binário único (.exe) do projeto, incluindo todos os assets de imagens.
    """
    base_dir = Path(__file__).parent.parent.resolve()
    main_py = base_dir / "main.py"
    assets_dir = base_dir / "assets"
    sep = ";" if sys.platform == "win32" else ":"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--name",
        "trabalho-final",
    ]
    # Empacota todas as imagens .png e .jpg da raiz de assets/
    for img in assets_dir.glob("*.[pj][np]g"):
        cmd.extend(["--add-data", f"{img}{sep}assets"])
    cmd.append(str(main_py))
    print("Executando:", " ".join(str(arg) for arg in cmd))
    subprocess.run(cmd, check=True)
