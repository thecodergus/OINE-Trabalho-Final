"""Utilitários para renderização comuns aos componentes da interface."""

import pygame
from typing import Tuple


def draw_circle_with_border(
    surface: pygame.Surface,
    center: Tuple[int, int],
    radius: int,
    fill_color: Tuple[int, int, int],
    border_color: Tuple[int, int, int],
    border_width: int = 1,
) -> None:
    """
    Desenha um círculo com borda.

    Args:
        surface: Superfície do Pygame onde desenhar
        center: Centro do círculo (x, y)
        radius: Raio do círculo
        fill_color: Cor de preenchimento (R, G, B)
        border_color: Cor da borda (R, G, B)
        border_width: Largura da borda (padrão: 1)
    """
    pygame.draw.circle(surface, fill_color, center, radius)
    pygame.draw.circle(surface, border_color, center, radius, border_width)


def draw_rounded_rect_with_border(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fill_color: Tuple[int, int, int],
    border_color: Tuple[int, int, int],
    border_width: int = 1,
    border_radius: int = 0,
) -> None:
    """
    Desenha um retângulo arredondado com borda.

    Args:
        surface: Superfície do Pygame onde desenhar
        rect: Retângulo a ser desenhado
        fill_color: Cor de preenchimento (R, G, B)
        border_color: Cor da borda (R, G, B)
        border_width: Largura da borda (padrão: 1)
        border_radius: Raio dos cantos arredondados (padrão: 0)
    """
    pygame.draw.rect(surface, fill_color, rect, border_radius=border_radius)
    pygame.draw.rect(
        surface, border_color, rect, border_width, border_radius=border_radius
    )