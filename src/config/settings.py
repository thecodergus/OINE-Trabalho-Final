from typing import Tuple, Dict, List
import os
from ..temperature_types import TemperatureScale

# Valores padrão de temperatura
TEMP_MIN_INICIAL = -100.0
TEMP_MAX_INICIAL = 100.0
VALOR_ATIVO_INICIAL = 20.0

# Base para cálculos nos botões + e -
BASE_MIN = -100.0
BASE_MAX = 100.0

# Limites para os valores de temperatura
TEMP_MIN_LIMITE = -100.0
TEMP_MAX_LIMITE = 100.0

# Strings para internacionalização
STRINGS = {
    "titulo_janela": "Simulação de Temperatura",
    "botao_mais": "+",
    "botao_menos": "−",
    "materiais": {"agua": "Água", "vidro": "Vidro", "aluminio": "Alumínio"},
    "escalas": {
        TemperatureScale.KELVIN: "K",
        TemperatureScale.CELSIUS: "°C",
        TemperatureScale.FAHRENHEIT: "°F",
    },
}


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Formato hexadecimal inválido: '{h}'")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


CORES = {
    "fundo": hex_to_rgb("#FFFFFF"),
    "texto": hex_to_rgb("#000000"),
    "indicador": hex_to_rgb("#FF0000"),
    "painel": (230, 230, 230),
    "painel_borda": (180, 180, 180),
    "botao_mais": hex_to_rgb("#4CAF50"),
    "botao_menos": hex_to_rgb("#F44336"),
    "termometro_borda": (80, 80, 80),
    "material_borda": (120, 120, 120),
    "material_fundo": (200, 200, 200),
    "botao_clique": hex_to_rgb("#CCCCCC"),
}

# Fontes dobradas
FONTES = {
    "titulo": ("Arial", 32, True),
    "rotulo": ("Arial", 24, False),
    "valor": ("Arial", 28, True),
}

TELA_LARGURA, TELA_ALTURA = 1024, 768

# Termômetros (movidos 200 pixels para a direita)
TERMOMETRO_DIM = (32, 293)
TERMOMETRO_Y = 111
TERMOMETRO_COUNT = 3
THUMB_RAIO = 18
BASE_RAIO = 25  # Aumentado de 22 para 25


# Defina um deslocamento fixo (em pixels) para mover os termômetros para a direita
DESLOCAMENTO_TERMOMETROS = 80  # Ajuste esse valor conforme necessário


def calcular_termometro_xs() -> Tuple[int, int, int]:
    margem_lateral_original = 159
    margem_lateral = int(margem_lateral_original * 0.8) + 50
    area_util = TELA_LARGURA - 2 * margem_lateral - 150
    espacamento = (area_util - TERMOMETRO_COUNT * TERMOMETRO_DIM[0]) // (
        TERMOMETRO_COUNT - 1
    )
    xs = [
        margem_lateral
        + i * (TERMOMETRO_DIM[0] + espacamento)
        + DESLOCAMENTO_TERMOMETROS
        for i in range(TERMOMETRO_COUNT)
    ]
    return (xs[0], xs[1], xs[2])


TERMOMETRO_XS = calcular_termometro_xs()

# Painel lateral direito (movido para cima, quase no topo)
PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H = 890, 10, 120, 180  # Y mudou de 77 para 10
BOTAO_RAIO = 18
BOTAO_Y = PAINEL_Y + 45
BOTAO_MAIS_X = PAINEL_X + 80
BOTAO_MENOS_X = PAINEL_X + 22
FAIXA_LABEL_Y = PAINEL_Y

# Materiais (parte inferior) - centralizados
MATERIAL_IMG_DIM = (120, 88)
MATERIAL_IMG_Y = 600
MATERIAL_LABEL_Y = MATERIAL_IMG_Y + MATERIAL_IMG_DIM[1] + 10


# Calcular posições dos materiais centralizadas
def calcular_material_xs() -> List[int]:
    # Calcular posições centralizadas
    espaco_total = TELA_LARGURA
    espaco_entre = (
        espaco_total - (3 * MATERIAL_IMG_DIM[0])
    ) // 4  # 4 espaços: antes, entre, entre, depois
    return [espaco_entre + i * (MATERIAL_IMG_DIM[0] + espaco_entre) for i in range(3)]


MATERIAL_XS = calcular_material_xs()

MATERIAIS = [
    (STRINGS["materiais"]["agua"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["vidro"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["aluminio"], "src/assets/imagem_generica.jpg"),
]
