import sys
import os
import pygame


def resource_path(relative_path: str) -> str:
    """
    Retorna o caminho absoluto para o asset, compatível com PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_path, relative_path)


def carregar_imagem(nome_arquivo: str) -> pygame.Surface | None:
    """
    Carrega uma imagem do diretório assets, convertendo para o formato ideal.
    """
    caminho = resource_path(f"assets/{nome_arquivo}")
    if not os.path.exists(caminho):
        print(f"ERRO: Arquivo não encontrado: {caminho}")
        return None
    imagem = pygame.image.load(caminho)
    if nome_arquivo.lower().endswith(".png"):
        return imagem.convert_alpha()
    return imagem.convert()
