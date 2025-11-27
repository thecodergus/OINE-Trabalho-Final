from pathlib import Path
import subprocess
import sys


def build() -> None:
    """
    Gera um binário único (.exe) do projeto, incluindo assets, módulos e dependências externas.
    Executa o PyInstaller com parâmetros otimizados para Windows e Pygame.
    """
    base_dir = Path(__file__).parent.parent.resolve()
    src_dir = base_dir / "src"
    main_py = base_dir / "main.py"
    assets_dir = src_dir / "assets"

    # Validação dos arquivos e diretórios
    required = [
        (assets_dir, "src/assets/"),
        (main_py, "main.py"),
    ]
    missing = [desc for path, desc in required if not path.exists()]
    if missing:
        print("❌ Arquivos/diretórios ausentes:", ", ".join(missing))
        sys.exit(1)

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
        "--hidden-import=pygame",
        "--hidden-import=src.core.state",
        "--hidden-import=src.components.thermometer",
        "--hidden-import=src.components.control_panel",
        "--hidden-import=src.components.material_display",
        "--hidden-import=src.interface.manager",
        "--hidden-import=src.utils.temperature_converter",
        "--hidden-import=src.config.settings",
        "--add-data",
        f"{assets_dir}{sep}assets",
        str(main_py),
    ]
    print("Executando:", " ".join(str(arg) for arg in cmd))
    subprocess.run(cmd, check=True)
