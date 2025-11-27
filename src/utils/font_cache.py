"""Módulo para cache de fontes do Pygame para melhorar performance."""

import pygame
from typing import Dict, Tuple
from ..config.settings import FONTES

# Cache global de fontes
_font_cache: Dict[Tuple[str, int, bool], pygame.font.Font] = {}


def get_cached_font(name: str, size: int, bold: bool = False) -> pygame.font.Font:
    """
    Retorna uma fonte do cache ou cria uma nova se não existir.

    Args:
        name: Nome da fonte
        size: Tamanho da fonte
        bold: Se a fonte deve ser em negrito

    Returns:
        pygame.font.Font: Objeto de fonte do Pygame
    """
    key = (name, size, bold)
    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(name, size, bold)
    return _font_cache[key]


def get_font_by_name(font_name: str) -> pygame.font.Font:
    """
    Retorna uma fonte pré-configurada do cache pelo nome.

    Args:
        font_name: Nome da configuração de fonte (e.g., "titulo", "rotulo", "valor")

    Returns:
        pygame.font.Font: Objeto de fonte do Pygame
    """
    if font_name not in FONTES:
        raise ValueError(f"Fonte '{font_name}' não encontrada em FONTES")

    font_config = FONTES[font_name]
    return get_cached_font(*font_config)


def clear_font_cache() -> None:
    """Limpa o cache de fontes."""
    global _font_cache
    _font_cache.clear()