import pygame
from typing import Tuple, Optional
from ..config.settings import (
    TERMOMETRO_Y,
    TERMOMETRO_DIM,
    CORES,
    THUMB_RAIO,
    BASE_RAIO,
    BORDA_ARREDONDADA,
    POSICAO_TEXTO_TERMOMETRO_Y,
)
from ..core.state import AppState
from ..temperature_types import TemperatureScale
from ..utils.font_cache import get_font_by_name
from ..utils.render_utils import draw_circle_with_border, draw_rounded_rect_with_border


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

            # Desenhar o fundo do termômetro
            pygame.draw.rect(
                self._cache_surface,
                (240, 240, 240),
                (0, 0, self.w, self.h),
                border_radius=BORDA_ARREDONDADA,
            )
            # Desenhar a borda do termômetro
            pygame.draw.rect(
                self._cache_surface,
                CORES["termometro_borda"],
                (0, 0, self.w, self.h),
                2,
                border_radius=BORDA_ARREDONDADA,
            )

    def valor_para_y(self, valor: float, temp_min: float, temp_max: float) -> int:
        # Converter os limites para a escala deste termômetro
        min_na_escala = self.converter_para_escala(temp_min, TemperatureScale.CELSIUS, self.escala)
        max_na_escala = self.converter_para_escala(temp_max, TemperatureScale.CELSIUS, self.escala)

        # Usar os limites específicos da escala para proporção
        escala_min, escala_max = self._obter_limites_escala()

        # Garantir que os valores estejam dentro dos limites da escala
        min_na_escala = max(min_na_escala, escala_min)
        max_na_escala = min(max_na_escala, escala_max)
        valor = max(min(valor, max_na_escala), min_na_escala)

        # Calcular proporção dentro da faixa visível
        if max_na_escala - min_na_escala == 0:
            ratio = 0
        else:
            ratio = (valor - min_na_escala) / (max_na_escala - min_na_escala)

        # Inverter porque y cresce para baixo na tela
        return int(self.y + self.h - ratio * self.h)

    def thumb_pos(self, state: AppState) -> Tuple[int, int]:
        # Todos os termômetros devem mostrar a mesma posição proporcional
        # baseada no valor ativo em relação aos limites atuais

        # Calcular a proporção do valor ativo em relação aos limites globais (em Celsius)
        if state.temp_max - state.temp_min == 0:
            ratio = 0.0
        else:
            # Converter o valor ativo para Celsius se necessário
            valor_celsius = state.valor_ativo
            if state.escala_ativa == TemperatureScale.KELVIN:
                valor_celsius = self.converter_para_escala(state.valor_ativo, TemperatureScale.KELVIN, TemperatureScale.CELSIUS)
            elif state.escala_ativa == TemperatureScale.FAHRENHEIT:
                valor_celsius = self.converter_para_escala(state.valor_ativo, TemperatureScale.FAHRENHEIT, TemperatureScale.CELSIUS)

            ratio = (valor_celsius - state.temp_min) / (state.temp_max - state.temp_min)

        # Aplicar a mesma proporção a todos os termômetros
        y = int(self.y + self.h - ratio * self.h)
        x = self.x + self.w // 2
        return (x, y)

    def converter_para_escala(self, valor: float, de: TemperatureScale, para: TemperatureScale) -> float:
        """Converte um valor de uma escala para outra."""
        if de == para:
            return valor

        # Converter para Celsius primeiro
        if de == TemperatureScale.KELVIN:
            valor_celsius = valor - 273.15
        elif de == TemperatureScale.FAHRENHEIT:
            valor_celsius = (valor - 32.0) * 5.0 / 9.0
        else:  # Celsius
            valor_celsius = valor

        # Converter de Celsius para a escala desejada
        if para == TemperatureScale.KELVIN:
            return valor_celsius + 273.15
        elif para == TemperatureScale.FAHRENHEIT:
            return valor_celsius * 9.0 / 5.0 + 32.0
        else:  # Celsius
            return valor_celsius

    def _obter_limites_escala(self) -> Tuple[float, float]:
        """Obtém os limites físicos significativos para cada escala."""
        if self.escala == TemperatureScale.KELVIN:
            # Kelvin começa em 0 (zero absoluto)
            return (0.0, 500.0)  # Exemplo de limite superior razoável
        elif self.escala == TemperatureScale.FAHRENHEIT:
            # Fahrenheit pode ir muito abaixo de zero
            return (-500.0, 1000.0)  # Limites amplos mas razoáveis
        else:  # Celsius
            # Celsius tem limites amplos também
            return (-300.0, 700.0)  # Limites amplos mas razoáveis

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
        # Usar a mesma proporção para todos os termômetros baseada no valor ativo
        if state.temp_max - state.temp_min == 0:
            nivel = 0.0
        else:
            # Converter o valor ativo para Celsius se necessário
            valor_celsius = state.valor_ativo
            if state.escala_ativa == TemperatureScale.KELVIN:
                valor_celsius = self.converter_para_escala(state.valor_ativo, TemperatureScale.KELVIN, TemperatureScale.CELSIUS)
            elif state.escala_ativa == TemperatureScale.FAHRENHEIT:
                valor_celsius = self.converter_para_escala(state.valor_ativo, TemperatureScale.FAHRENHEIT, TemperatureScale.CELSIUS)

            nivel = (valor_celsius - state.temp_min) / (state.temp_max - state.temp_min)

        # Garantir que o nível esteja entre 0 e 1
        nivel = max(0.0, min(1.0, nivel))

        nivel_px = int(self.h * nivel)
        # Garantir que o retângulo de preenchimento não ultrapasse os limites do termômetro
        if nivel_px > self.h:
            nivel_px = self.h
        rect_preenchido = pygame.Rect(
            self.x, self.y + self.h - nivel_px, self.w, nivel_px
        )
        pygame.draw.rect(surf, CORES["indicador"], rect_preenchido, border_radius=BORDA_ARREDONDADA)

    def _render_thumb(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o thumb (círculo móvel)."""
        thumb_x, thumb_y = self.thumb_pos(state)
        draw_circle_with_border(
            surf, (thumb_x, thumb_y), THUMB_RAIO, CORES["indicador"], CORES["texto"], 2
        )

    def _render_base(self, surf: pygame.Surface) -> None:
        """Renderiza a base (bolinha) do termômetro."""
        base_x, base_y = self.base_pos()
        draw_circle_with_border(
            surf, (base_x, base_y), BASE_RAIO, CORES["indicador"], CORES["texto"], 2
        )

    def _render_value_text(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o texto com o valor da temperatura."""
        valor = state.valores()[self.escala]
        fonte = get_font_by_name("valor")
        txt = fonte.render(f"{valor:.2f} {self.escala.symbol}", True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, self.y - POSICAO_TEXTO_TERMOMETRO_Y))
