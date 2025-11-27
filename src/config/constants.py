"""Constantes numéricas e gerais da aplicação."""

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

# Dimensões da tela
TELA_LARGURA, TELA_ALTURA = 1024, 768

# Dimensões e posições dos termômetros
TERMOMETRO_DIM = (32, 293)
TERMOMETRO_Y = 111
TERMOMETRO_COUNT = 3
THUMB_RAIO = 18
BASE_RAIO = 25  # Aumentado de 22 para 25
DESLOCAMENTO_TERMOMETROS = 80  # Ajuste esse valor conforme necessário

# Dimensões e posições dos materiais
MATERIAL_IMG_DIM = (120, 88)
MATERIAL_IMG_Y = 600
MATERIAL_LABEL_Y = MATERIAL_IMG_Y + MATERIAL_IMG_DIM[1] + 10

# Dimensões e posições do painel de controle
PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H = 890, 10, 120, 180  # Y mudou de 77 para 10
BOTAO_RAIO = 18
BOTAO_Y = PAINEL_Y + 45
BOTAO_MAIS_X = PAINEL_X + 80
BOTAO_MENOS_X = PAINEL_X + 22
FAIXA_LABEL_Y = PAINEL_Y
