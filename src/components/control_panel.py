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
    FONTES,
    BOTAO_RAIO,
    BOTAO_Y,
    BOTAO_MAIS_X,
    BOTAO_MENOS_X,
    FAIXA_LABEL_Y,
)
from ..core.state import AppState
from ..temperature_types import TemperatureScale


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

    def _handle_mouse_down(self, event: pygame.event.Event, state: AppState) -> AppState:
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
        # Calcular a distância dos valores atuais em relação à base
        distancia_min = state.temp_min - BASE_MIN
        distancia_max = state.temp_max - BASE_MAX

        # Multiplicar as distâncias por 2
        nova_distancia_min = distancia_min * 2
        nova_distancia_max = distancia_max * 2

        # Calcular os novos valores
        novo_min = BASE_MIN + nova_distancia_min
        novo_max = BASE_MAX + nova_distancia_max

        # Aplicar limites
        novo_min = max(novo_min, -100.0)
        novo_max = max(novo_max, 100.0)

        # Atualizar também o valor ativo (aumenta proporcionalmente)
        centro_atual = (state.temp_min + state.temp_max) / 2
        centro_novo = (novo_min + novo_max) / 2
        distancia_centro = state.valor_ativo - centro_atual
        nova_distancia_centro = distancia_centro * 2
        novo_valor = centro_novo + nova_distancia_centro
        # Garantir que o valor esteja dentro dos novos limites
        novo_valor = max(novo_min, min(novo_max, novo_valor))

        return AppState(
            temp_min=novo_min,
            temp_max=novo_max,
            escala_ativa=state.escala_ativa,
            valor_ativo=novo_valor,
            arrastando=state.arrastando,
            botao_mais_pressionado=True,
            botao_menos_pressionado=state.botao_menos_pressionado,
        )

    def _handle_minus_button(self, state: AppState) -> AppState:
        # Calcular a distância dos valores atuais em relação à base
        distancia_min = state.temp_min - BASE_MIN
        distancia_max = state.temp_max - BASE_MAX

        # Dividir as distâncias por 2
        nova_distancia_min = distancia_min / 2
        nova_distancia_max = distancia_max / 2

        # Calcular os novos valores
        novo_min = BASE_MIN + nova_distancia_min
        novo_max = BASE_MAX + nova_distancia_max

        # Aplicar limites
        novo_min = max(novo_min, -100.0)
        novo_max = max(novo_max, 100.0)

        # Atualizar também o valor ativo (diminui proporcionalmente)
        centro_atual = (state.temp_min + state.temp_max) / 2
        centro_novo = (novo_min + novo_max) / 2
        distancia_centro = state.valor_ativo - centro_atual
        nova_distancia_centro = distancia_centro / 2
        novo_valor = centro_novo + nova_distancia_centro
        # Garantir que o valor esteja dentro dos novos limites
        novo_valor = max(novo_min, min(novo_max, novo_valor))

        return AppState(
            temp_min=novo_min,
            temp_max=novo_max,
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
        """Renderiza a label com os valores de temperatura."""
        escala_ativa = state.escala_ativa
        min_convertido = converter(
            state.temp_min, TemperatureScale.CELSIUS, escala_ativa
        )
        max_convertido = converter(
            state.temp_max, TemperatureScale.CELSIUS, escala_ativa
        )

        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(
            f"({int(min_convertido)}, {int(max_convertido)}) {escala_ativa.symbol}",
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
        pygame.draw.circle(surf, cor_botao_mais, self.botao_mais.center, BOTAO_RAIO)
        pygame.draw.circle(surf, CORES["texto"], self.botao_mais.center, BOTAO_RAIO, 2)
        fonte_b = pygame.font.SysFont(*FONTES["titulo"])
        txt_mais = fonte_b.render("+", True, CORES["texto"])
        surf.blit(
            txt_mais,
            (
                self.botao_mais.centerx - txt_mais.get_width() // 2,
                self.botao_mais.centery - txt_mais.get_height() // 2,
            ),
        )

        # Renderizar botão -
        pygame.draw.circle(surf, cor_botao_menos, self.botao_menos.center, BOTAO_RAIO)
        pygame.draw.circle(surf, CORES["texto"], self.botao_menos.center, BOTAO_RAIO, 2)
        txt_menos = fonte_b.render("−", True, CORES["texto"])
        surf.blit(
            txt_menos,
            (
                self.botao_menos.centerx - txt_menos.get_width() // 2,
                self.botao_menos.centery - txt_menos.get_height() // 2,
            ),
        )
