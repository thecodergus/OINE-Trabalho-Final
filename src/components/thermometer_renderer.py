import pygame
from typing import Tuple, Optional
from ..config.settings import (
    TERMOMETRO_Y,
    TERMOMETRO_DIM,
    CORES,
    THUMB_RAIO,
    BASE_RAIO,
    FONTES,
)
from ..core.state import AppState
from ..temperature_types import TemperatureScale


class TermometroRenderer:
    def __init__(self, x: int, escala: TemperatureScale) -> None:
        self.x = x
        self.y = TERMOMETRO_Y
        self.w, self.h = TERMOMETRO_DIM
        self.escala = escala
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self._cache_surface: Optional[pygame.Surface] = None
        self._cache_rect: Optional[pygame.Rect] = None

    def _criar_cache(self) -> None:
        if self._cache_surface is None or self._cache_rect != self.rect:
            # Criar superfície apenas para o termômetro (sem a base)
            self._cache_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self._cache_rect = self.rect.copy()

            pygame.draw.rect(
                self._cache_surface,
                (240, 240, 240),
                (0, 0, self.w, self.h),
                border_radius=8,
            )
            pygame.draw.rect(
                self._cache_surface,
                CORES["termometro_borda"],
                (0, 0, self.w, self.h),
                2,
                border_radius=8,
            )

    def valor_para_y(self, valor: float, temp_min: float, temp_max: float) -> int:
        ratio = (valor - temp_min) / (temp_max - temp_min)
        return int(self.y + self.h - ratio * self.h)

    def thumb_pos(self, state: AppState) -> Tuple[int, int]:
        valor = state.valores()[self.escala]
        y = self.valor_para_y(valor, state.temp_min, state.temp_max)
        x = self.x + self.w // 2
        return (x, y)

    def base_pos(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h + BASE_RAIO)

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        self._criar_cache()

        # Desenhar o termômetro
        if self._cache_surface:
            surf.blit(self._cache_surface, (self.x, self.y))

        # Desenhar o nível de preenchimento
        self._render_fill_level(surf, state)

        # Desenhar o thumb (círculo móvel)
        self._render_thumb(surf, state)

        # Desenhar a base (bolinha) separadamente, sobrepondo o início do termômetro
        self._render_base(surf)

        # Desenhar o texto com o valor
        self._render_value_text(surf, state)

    def _render_fill_level(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o nível de preenchimento do termômetro."""
        valor = state.valores()[self.escala]
        nivel = (valor - state.temp_min) / (state.temp_max - state.temp_min)
        nivel_px = int(self.h * nivel)
        rect_preenchido = pygame.Rect(
            self.x, self.y + self.h - nivel_px, self.w, nivel_px
        )
        pygame.draw.rect(surf, CORES["indicador"], rect_preenchido, border_radius=8)

    def _render_thumb(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o thumb (círculo móvel)."""
        thumb_x, thumb_y = self.thumb_pos(state)
        pygame.draw.circle(surf, CORES["indicador"], (thumb_x, thumb_y), THUMB_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (thumb_x, thumb_y), THUMB_RAIO, 2)

    def _render_base(self, surf: pygame.Surface) -> None:
        """Renderiza a base (bolinha) do termômetro."""
        base_x, base_y = self.base_pos()
        pygame.draw.circle(surf, CORES["indicador"], (base_x, base_y), BASE_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (base_x, base_y), BASE_RAIO, 2)

    def _render_value_text(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o texto com o valor da temperatura."""
        valor = state.valores()[self.escala]
        fonte = pygame.font.SysFont(*FONTES["valor"])
        txt = fonte.render(f"{valor:.2f} {self.escala.symbol}", True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, self.y - 48))
