"""Cálculos e definições de layout da aplicação."""

from .constants import (
    TELA_LARGURA,
    TELA_ALTURA,
    TERMOMETRO_COUNT,
    TERMOMETRO_DIM,
    DESLOCAMENTO_TERMOMETROS,
    MATERIAL_IMG_DIM,
    PAINEL_X,
    PAINEL_W,
)

def calcular_termometro_xs() -> tuple[int, int, int]:
    """Calcula as posições X dos termômetros."""
    margem_lateral = int(159 * 0.8) + 50
    area_util = TELA_LARGURA - 2 * margem_lateral - 150
    espacamento = (area_util - TERMOMETRO_COUNT * TERMOMETRO_DIM[0]) // (TERMOMETRO_COUNT - 1)
    xs = [
        margem_lateral + i * (TERMOMETRO_DIM[0] + espacamento)
        for i in range(TERMOMETRO_COUNT)
    ]
    return tuple(xs)

TERMOMETRO_XS = calcular_termometro_xs()

def calcular_material_xs() -> list[int]:
    """Calcula as posições X dos materiais centralizados."""
    # Calcular posições centralizadas
    espaco_total = TELA_LARGURA
    espaco_entre = (
        espaco_total - (3 * MATERIAL_IMG_DIM[0])
    ) // 4  # 4 espaços: antes, entre, entre, depois
    return [espaco_entre + i * (MATERIAL_IMG_DIM[0] + espaco_entre) for i in range(3)]

MATERIAL_XS = calcular_material_xs()
