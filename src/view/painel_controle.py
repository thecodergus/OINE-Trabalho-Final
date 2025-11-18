from typing import Tuple
import pygame
from ..model.state import AppState
from .slider import ControleSlider
from .label import LabelDinamico


class PainelControle:
    """Painel de controle: organiza slider e label conforme wireframe."""

    def __init__(self, panel_rect: Tuple[int, int, int, int]) -> None:
        self.panel_rect = pygame.Rect(panel_rect)
        # Layout: slider centralizado, label acima
        slider_x = self.panel_rect.x + 50
        slider_y = self.panel_rect.y + 120
        self.slider = ControleSlider(
            rect=(slider_x, slider_y, 200, 8), min_value=-50.0, max_value=150.0
        )
        label_x = self.panel_rect.x + (self.panel_rect.width // 2)
        label_y = slider_y - 52  # 32 px label + 20 px espaçamento
        self.label = LabelDinamico(center=(label_x, label_y))

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        """Delegação de eventos para o slider (Controller)."""
        return self.slider.handle_event(event, state)

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        """Desenha o painel, slider e label."""
        # Painel de fundo
        pygame.draw.rect(surface, (220, 220, 220), self.panel_rect)
        pygame.draw.rect(surface, (180, 180, 180), self.panel_rect, width=2)
        # Slider
        self.slider.render(surface, state)
        # Label dinâmico
        self.label.render(surface, state)
