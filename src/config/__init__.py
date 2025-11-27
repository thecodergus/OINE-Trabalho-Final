"""Módulo de configuração da aplicação."""

# Importar e reexportar os módulos de configuração
from .constants import *
from .colors import *
from .strings import *
from .layout import *

# Fontes dobradas - Mantém aqui por ser uma configuração simples e específica
FONTES = {
    "titulo": ("Arial", 32, True),
    "rotulo": ("Arial", 24, False),
    "valor": ("Arial", 28, True),
}

# MATERIAIS - depende de STRINGS
MATERIAIS = [
    (STRINGS["materiais"]["agua"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["vidro"], "src/assets/imagem_generica.jpg"),
    (STRINGS["materiais"]["aluminio"], "src/assets/imagem_generica.jpg"),
]
