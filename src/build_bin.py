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
    assets_png = src_dir / "assets" / "wireframe.png"
    controller_dir = src_dir / "controller"
    model_dir = src_dir / "model"
    view_dir = src_dir / "view"

    # Validação dos arquivos e diretórios
    required = [
        (assets_png, "src/assets/wireframe.png"),
        (controller_dir, "src/controller/"),
        (model_dir, "src/model/"),
        (view_dir, "src/view/"),
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
        "--hidden-import=controller.slider_controllet",
        "--hidden-import=model.state",
        "--hidden-import=view.label",
        "--hidden-import=view.painel_controle",
        "--hidden-import=view.slider",
        "--add-data",
        f"{assets_png}{sep}assets",
        "--add-data",
        f"{controller_dir}{sep}controller",
        "--add-data",
        f"{model_dir}{sep}model",
        "--add-data",
        f"{view_dir}{sep}view",
        str(main_py),
    ]
    print("Executando:", " ".join(str(arg) for arg in cmd))
    subprocess.run(cmd, check=True)
