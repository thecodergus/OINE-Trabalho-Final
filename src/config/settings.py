# Arquivo mantido temporariamente para compatibilidade com imports antigos
# TODO: Remover após atualizar todos os imports

from .constants import *
from .colors import *
from .strings import *
from .layout import *

# Reexportar FONTES do __init__.py
from . import FONTES

# Reexportar MATERIAIS que depende de STRINGS
from . import MATERIAIS
