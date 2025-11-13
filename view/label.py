from typing import Tuple
import pygame
from model.state import AppState

class LabelDinamico:
    """Label dinâmico que exibe o valor atual do slider."""
    def __init__(self, center: Tuple[int, int]) -> None:
        self.center = center
        self.font = pygame.font.SysFont("Arial", 32, bold=True)

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        """Desenha o label centralizado acima do slider."""
        text = f"{state.slider_value:.1f} °C"
        label_surf = self.font.render(text, True, (30, 30, 30))
        rect = label_surf.get_rect(center=self.center)
        surface.blit(label_surf, rect)
