from typing import Tuple, Dict, List
import os

# Strings para internacionalização
STRINGS = {
    "titulo_janela": "Simulação de Temperatura",
    "botao_mais": "+",
    "botao_menos": "−",
    "materiais": {
        "agua": "Água",
        "vidro": "Vidro",
        "aluminio": "Alumínio"
    },
    "escalas": {
        "kelvin": "K",
        "celsius": "°C",
        "fahrenheit": "°F"
    }
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

# Termômetros
TERMOMETRO_DIM = (32, 293)
TERMOMETRO_Y = 111
TERMOMETRO_COUNT = 3
TERMOMETRO_ESCALAS = [STRINGS["escalas"]["kelvin"], STRINGS["escalas"]["celsius"], STRINGS["escalas"]["fahrenheit"]]
THUMB_RAIO = 18
BASE_RAIO = 22

# Espaçamento dinâmico centralizado
def calcular_termometro_xs() -> Tuple[int, int, int]:
    margem_lateral = 159
    area_util = TELA_LARGURA - 2 * margem_lateral
    espacamento = (area_util - TERMOMETRO_COUNT * TERMOMETRO_DIM[0]) // (TERMOMETRO_COUNT - 1)
    xs = [
        margem_lateral + i * (TERMOMETRO_DIM[0] + espacamento)
        for i in range(TERMOMETRO_COUNT)
    ]
    return (xs[0], xs[1], xs[2])

TERMOMETRO_XS = calcular_termometro_xs()

# Painel lateral direito
PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H = 860, 77, 120, 180
BOTAO_RAIO = 18
BOTAO_Y = PAINEL_Y + 60
BOTAO_MAIS_X = PAINEL_X + 80
BOTAO_MENOS_X = PAINEL_X + 22
FAIXA_LABEL_Y = PAINEL_Y + 20

# Materiais (parte inferior)
MATERIAL_IMG_DIM = (120, 88)
MATERIAL_IMG_Y = 549
MATERIAL_LABEL_Y = MATERIAL_IMG_Y - 48
MATERIAL_XS = [159, 444, 717]
MATERIAIS = [
    (STRINGS["materiais"]["agua"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["vidro"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["aluminio"], "src/assets/imagem_generica.jpg"),
]
