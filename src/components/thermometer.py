import pygame
from typing import Tuple, Optional
from ..config.settings import (
    TERMOMETRO_Y,
    TERMOMETRO_DIM,
    CORES,
    THUMB_RAIO,
    BASE_RAIO,
    FONTES,
    TERMOMETRO_XS,
    STRINGS,
)
from ..core.state import AppState
from ..temperature_types import TemperatureScale


class Termometro:
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

    def y_para_valor(self, y: int, temp_min: float, temp_max: float) -> float:
        y = max(self.y, min(self.y + self.h, y))
        ratio = (self.y + self.h - y) / self.h
        return temp_min + ratio * (temp_max - temp_min)

    def thumb_pos(self, state: AppState) -> Tuple[int, int]:
        valor = state.valores()[self.escala]
        y = self.valor_para_y(valor, state.temp_min, state.temp_max)
        x = self.x + self.w // 2
        return (x, y)

    def base_pos(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h + BASE_RAIO)

    def handle_event(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
        thumb_x, thumb_y = self.thumb_pos(state)
        mouse_x, mouse_y = getattr(event, "pos", (None, None))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                mouse_x is not None
                and mouse_y is not None
                and (thumb_x - THUMB_RAIO) <= mouse_x <= (thumb_x + THUMB_RAIO)
                and (thumb_y - THUMB_RAIO) <= mouse_y <= (thumb_y + THUMB_RAIO)
            ):
                return AppState(
                    temp_min=state.temp_min,
                    temp_max=state.temp_max,
                    escala_ativa=self.escala,
                    valor_ativo=state.valor_ativo,
                    arrastando=self.escala.value,
                    botao_mais_pressionado=state.botao_mais_pressionado,
                    botao_menos_pressionado=state.botao_menos_pressionado,
                )
        elif event.type == pygame.MOUSEBUTTONUP:
            if state.arrastando == self.escala.value:
                return AppState(
                    temp_min=state.temp_min,
                    temp_max=state.temp_max,
                    escala_ativa=state.escala_ativa,
                    valor_ativo=state.valor_ativo,
                    arrastando=None,
                    botao_mais_pressionado=state.botao_mais_pressionado,
                    botao_menos_pressionado=state.botao_menos_pressionado,
                )
        elif event.type == pygame.MOUSEMOTION:
            if state.arrastando == self.escala.value and mouse_y is not None:
                novo_valor = self.y_para_valor(mouse_y, state.temp_min, state.temp_max)
                novo_valor = state.clamp_valor(novo_valor)

                # Verificar se está tentando aumentar além do limite máximo
                if novo_valor > state.valor_ativo and not state.pode_aumentar():
                    return None

                # Verificar se está tentando diminuir além do limite mínimo
                if novo_valor < state.valor_ativo and not state.pode_diminuir():
                    return None

                return AppState(
                    temp_min=state.temp_min,
                    temp_max=state.temp_max,
                    escala_ativa=state.escala_ativa,  # Manter a escala ativa original
                    valor_ativo=novo_valor,
                    arrastando=self.escala.value,
                    botao_mais_pressionado=state.botao_mais_pressionado,
                    botao_menos_pressionado=state.botao_menos_pressionado,
                )
        return None

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        self._criar_cache()

        # Desenhar o termômetro
        if self._cache_surface:
            surf.blit(self._cache_surface, (self.x, self.y))

        # Desenhar o nível de preenchimento
        valor = state.valores()[self.escala]
        nivel = (valor - state.temp_min) / (state.temp_max - state.temp_min)
        nivel_px = int(self.h * nivel)
        rect_preenchido = pygame.Rect(
            self.x, self.y + self.h - nivel_px, self.w, nivel_px
        )
        pygame.draw.rect(surf, CORES["indicador"], rect_preenchido, border_radius=8)

        # Desenhar o thumb (círculo móvel)
        thumb_x, thumb_y = self.thumb_pos(state)
        pygame.draw.circle(surf, CORES["indicador"], (thumb_x, thumb_y), THUMB_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (thumb_x, thumb_y), THUMB_RAIO, 2)

        # Desenhar a base (bolinha) separadamente, sobrepondo o início do termômetro
        base_x = self.x + self.w // 2
        base_y = (
            self.y + self.h + BASE_RAIO - 15
        )  # Movido 10px para cima (de -5 para -15)
        pygame.draw.circle(surf, CORES["indicador"], (base_x, base_y), BASE_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (base_x, base_y), BASE_RAIO, 2)

        # Desenhar o texto com o valor
        fonte = pygame.font.SysFont(*FONTES["valor"])
        txt = fonte.render(f"{valor:.2f} {self.escala.symbol}", True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, self.y - 48))
