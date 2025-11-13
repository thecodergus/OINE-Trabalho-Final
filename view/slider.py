from typing import Tuple
import pygame
from model.state import AppState

class ControleSlider:
    """Slider horizontal de temperatura, interativo e funcional."""
    def __init__(self, rect: Tuple[int, int, int, int], min_value: float, max_value: float) -> None:
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.thumb_radius = 16
        self.dragging = False

    def value_to_pos(self, value: float) -> int:
        """Converte valor do slider para posição x do thumb."""
        ratio = (value - self.min_value) / (self.max_value - self.min_value)
        return int(self.rect.x + ratio * self.rect.width)

    def pos_to_value(self, x: int) -> float:
        """Converte posição x do mouse para valor do slider."""
        ratio = (x - self.rect.x) / self.rect.width
        value = self.min_value + ratio * (self.max_value - self.min_value)
        return max(self.min_value, min(self.max_value, value))

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        """Processa eventos do mouse e retorna novo estado imutável."""
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if self._thumb_collidepoint(event.pos, state):
                    self.dragging = True
            case pygame.MOUSEBUTTONUP:
                self.dragging = False
            case pygame.MOUSEMOTION if self.dragging:
                new_value = self.pos_to_value(event.pos[0])
                # Retorna novo estado imutável
                from dataclasses import replace
                return replace(state, slider_value=new_value)
        return state

    def _thumb_collidepoint(self, pos: Tuple[int, int], state: AppState) -> bool:
        """Verifica se o mouse está sobre o thumb do slider."""
        thumb_x = self.value_to_pos(state.slider_value)
        thumb_y = self.rect.y + self.rect.height // 2
        dx = pos[0] - thumb_x
        dy = pos[1] - thumb_y
        return dx * dx + dy * dy <= self.thumb_radius * self.thumb_radius

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        """Desenha o slider (trilho e thumb)."""
        # Trilho
        pygame.draw.rect(surface, (160, 160, 160), self.rect, border_radius=4)
        # Thumb
        thumb_x = self.value_to_pos(state.slider_value)
        thumb_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(surface, (80, 120, 200), (thumb_x, thumb_y), self.thumb_radius)
        pygame.draw.circle(surface, (40, 40, 40), (thumb_x, thumb_y), self.thumb_radius, width=2)
