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
        # Multiplicar ambos os valores por 2
        new_min = state.temp_min * 2
        new_max = state.temp_max * 2

        # Aplicar limites
        # O valor negativo não pode ser maior que -50 (ex: -40, -30 não são permitidos)
        # Mas pode ser menor (ex: -100, -200, etc.)
        # O valor positivo pode ser qualquer valor positivo (sem limite inferior nem superior)
        # new_max não precisa de limite mínimo pois pode ser qualquer valor positivo

        # Ajustar o valor ativo proporcionalmente
        if state.temp_max - state.temp_min > 0:
            position_ratio = (state.valor_ativo - state.temp_min) / (state.temp_max - state.temp_min)
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
        # Dividir ambos os valores por 2
        new_min = state.temp_min / 2
        new_max = state.temp_max / 2

        # Aplicar limites para continuar até chegar a (-50, 50)
        # O valor negativo deve se aproximar de -50 (mas não ultrapassar para valores mais positivos)
        # Se o valor negativo for maior que -50 (ex: -25), deve ficar em -50
        # Se o valor negativo for menor que -50 (ex: -100), dividir por 2 o aproxima de -50
        if new_min > TEMP_MIN_LIMITE:  # Se for maior que -50 (ex: -25)
            new_min = TEMP_MIN_LIMITE   # Fica em -50

        # O valor positivo deve se aproximar de 50 (mas não ultrapassar para valores menores)
        # Se o valor positivo for menor que 50 (ex: 25), deve ficar em 50
        # Se o valor positivo for maior que 50 (ex: 100), dividir por 2 o aproxima de 50
        if new_max < 50.0:  # Se for menor que 50 (ex: 25)
            new_max = 50.0   # Fica em 50

        # Ajustar o valor ativo proporcionalmente
        if state.temp_max - state.temp_min > 0:
            position_ratio = (state.valor_ativo - state.temp_min) / (state.temp_max - state.temp_min)
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
