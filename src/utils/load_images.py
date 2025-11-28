import sys
import os


def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto para o asset, compatível com PyInstaller.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
