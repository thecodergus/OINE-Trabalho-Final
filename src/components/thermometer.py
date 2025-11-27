import pygame
from typing import Tuple, Optional
from ..core.state import AppState
from ..temperature_types import TemperatureScale
from .thermometer_renderer import TermometroRenderer
from ..config.settings import THUMB_RAIO


class Termometro:
    def __init__(self, x: int, escala: TemperatureScale) -> None:
        self.escala = escala
        self.renderer = TermometroRenderer(x, escala)

    def valor_para_y(self, valor: float, temp_min: float, temp_max: float) -> int:
        return self.renderer.valor_para_y(valor, temp_min, temp_max)

    def thumb_pos(self, state: AppState) -> Tuple[int, int]:
        return self.renderer.thumb_pos(state)

    def handle_event(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_down(event, state)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._handle_mouse_up(event, state)
        elif event.type == pygame.MOUSEMOTION:
            return self._handle_mouse_motion(event, state)
        return None

    def _handle_mouse_down(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
        thumb_x, thumb_y = self.thumb_pos(state)
        mouse_x, mouse_y = getattr(event, "pos", (None, None))
        
        # Verificar clique no thumb (círculo móvel)
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
        return None

    def _handle_mouse_up(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
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
        return None

    def _handle_mouse_motion(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
        if state.arrastando == self.escala.value and getattr(event, "pos", None):
            mouse_x, mouse_y = event.pos
            novo_valor = self.y_para_valor(mouse_y, state.temp_min, state.temp_max)
            novo_valor = state.clamp_valor(novo_valor)

            # Verificar se está tentando aumentar além do limite máximo
            if novo_valor > state.valor_ativo and not state.pode_aumentar(
                novo_valor
            ):
                return None

            # Verificar se está tentando diminuir além do limite mínimo
            if novo_valor < state.valor_ativo and not state.pode_diminuir(
                novo_valor
            ):
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

    def y_para_valor(self, y: int, temp_min: float, temp_max: float) -> float:
        y = max(self.renderer.y, min(self.renderer.y + self.renderer.h, y))
        ratio = (self.renderer.y + self.renderer.h - y) / self.renderer.h
        return temp_min + ratio * (temp_max - temp_min)

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        self.renderer.render(surf, state)
