import pygame

from ..utils.temperature_converter import converter
from ..config.settings import (
    BASE_MAX,
    BASE_MIN,
    PAINEL_X,
    PAINEL_Y,
    PAINEL_W,
    PAINEL_H,
    CORES,
    BOTAO_RAIO,
    BOTAO_Y,
    BOTAO_MAIS_X,
    BOTAO_MENOS_X,
    FAIXA_LABEL_Y,
    TEMP_MIN_LIMITE,
    TEMP_MAX_LIMITE,
)
from ..core.state import AppState
from ..temperature_types import TemperatureScale
from ..utils.font_cache import get_font_by_name
from ..utils.render_utils import draw_circle_with_border


class PainelControle:
    def __init__(self, rect: tuple) -> None:
        self.panel_rect = pygame.Rect(rect)
        self.botao_mais = pygame.Rect(
            BOTAO_MAIS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )
        self.botao_menos = pygame.Rect(
            BOTAO_MENOS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        if state.arrastando is not None:
            return state

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_down(event, state)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._handle_mouse_up(event, state)

        return state

    def _handle_mouse_down(
        self, event: pygame.event.Event, state: AppState
    ) -> AppState:
        if self.botao_mais.collidepoint(event.pos):
            return self._handle_plus_button(state)
        elif self.botao_menos.collidepoint(event.pos):
            return self._handle_minus_button(state)
        return state

    def _handle_mouse_up(self, event: pygame.event.Event, state: AppState) -> AppState:
        if state.botao_mais_pressionado or state.botao_menos_pressionado:
            return AppState(
                temp_min=state.temp_min,
                temp_max=state.temp_max,
                escala_ativa=state.escala_ativa,
                valor_ativo=state.valor_ativo,
                arrastando=state.arrastando,
                botao_mais_pressionado=False,
                botao_menos_pressionado=False,
            )
        return state

    def _handle_plus_button(self, state: AppState) -> AppState:
        # Expandir o intervalo de temperatura multiplicando por 2
        range_center = (state.temp_min + state.temp_max) / 2
        range_size = state.temp_max - state.temp_min

        # Dobrar o tamanho do intervalo
        new_range_size = range_size * 2
        new_min = range_center - new_range_size / 2
        new_max = range_center + new_range_size / 2

        # Aplicar limites
        new_min = max(new_min, TEMP_MIN_LIMITE)
        new_max = min(new_max, TEMP_MAX_LIMITE)

        # Ajustar o valor ativo proporcionalmente
        if range_size > 0:
            position_ratio = (state.valor_ativo - state.temp_min) / range_size
            novo_valor = new_min + position_ratio * (new_max - new_min)
        else:
            novo_valor = state.valor_ativo

        return AppState(
            temp_min=new_min,
            temp_max=new_max,
            escala_ativa=state.escala_ativa,
            valor_ativo=novo_valor,
            arrastando=state.arrastando,
            botao_mais_pressionado=True,
            botao_menos_pressionado=state.botao_menos_pressionado,
        )

    def _handle_minus_button(self, state: AppState) -> AppState:
        # Contrair o intervalo de temperatura dividindo por 2
        range_center = (state.temp_min + state.temp_max) / 2
        range_size = state.temp_max - state.temp_min

        # Dividir o tamanho do intervalo por 2
        new_range_size = range_size / 2
        new_min = range_center - new_range_size / 2
        new_max = range_center + new_range_size / 2

        # Aplicar limites
        new_min = max(new_min, TEMP_MIN_LIMITE)
        new_max = min(new_max, TEMP_MAX_LIMITE)

        # Ajustar o valor ativo proporcionalmente
        if range_size > 0:
            position_ratio = (state.valor_ativo - state.temp_min) / range_size
            novo_valor = new_min + position_ratio * (new_max - new_min)
        else:
            novo_valor = state.valor_ativo

        return AppState(
            temp_min=new_min,
            temp_max=new_max,
            escala_ativa=state.escala_ativa,
            valor_ativo=novo_valor,
            arrastando=state.arrastando,
            botao_mais_pressionado=state.botao_mais_pressionado,
            botao_menos_pressionado=True,
        )

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Desenha apenas os botões e o texto
        self._render_label(surf, state)
        self._render_buttons(surf, state)

    def _render_label(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza a label com os valores de temperatura em Celsius."""
        # Sempre mostrar em Celsius, independentemente da escala ativa
        min_celsius = state.temp_min
        max_celsius = state.temp_max

        fonte = get_font_by_name("rotulo")
        txt = fonte.render(
            f"({int(min_celsius)}, {int(max_celsius)}) °C",
            True,
            CORES["texto"],
        )
        surf.blit(txt, (PAINEL_X + (PAINEL_W - txt.get_width()) // 2, FAIXA_LABEL_Y))

    def _render_buttons(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza os botões + e -."""
        cor_botao_mais = (
            CORES["botao_clique"]
            if state.botao_mais_pressionado
            else CORES["botao_mais"]
        )
        cor_botao_menos = (
            CORES["botao_clique"]
            if state.botao_menos_pressionado
            else CORES["botao_menos"]
        )

        # Renderizar botão +
        draw_circle_with_border(
            surf, self.botao_mais.center, BOTAO_RAIO, cor_botao_mais, CORES["texto"], 2
        )
        fonte_b = get_font_by_name("titulo")
        txt_mais = fonte_b.render("+", True, CORES["texto"])
        surf.blit(
            txt_mais,
            (
                self.botao_mais.centerx - txt_mais.get_width() // 2,
                self.botao_mais.centery - txt_mais.get_height() // 2,
            ),
        )

        # Renderizar botão -
        draw_circle_with_border(
            surf, self.botao_menos.center, BOTAO_RAIO, cor_botao_menos, CORES["texto"], 2
        )
        txt_menos = fonte_b.render("−", True, CORES["texto"])
        surf.blit(
            txt_menos,
            (
                self.botao_menos.centerx - txt_menos.get_width() // 2,
                self.botao_menos.centery - txt_menos.get_height() // 2,
            ),
        )
