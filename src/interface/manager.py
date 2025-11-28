from dataclasses import dataclass, field
from typing import ClassVar, List
import pygame
from config.colors import CORES
from src.config.settings import (
    TERMOMETRO_XS,
    STRINGS,
    PAINEL_X,
    PAINEL_Y,
    PAINEL_W,
    PAINEL_H,
    MATERIAL_XS,
    MATERIAIS,
)
from src.components.thermometer import Termometro
from src.components.control_panel import PainelControle
from src.components.material_display import MaterialDisplay, MaterialType
from src.core.state import AppState
from src.temperature_types import TemperatureScale


@dataclass(slots=True)
class InterfaceManager:
    """
    Orquestrador da interface gráfica e do fluxo de eventos do jogo/simulação.
    Coordena termômetros, painel de controle e displays de materiais.
    Segue princípios de imutabilidade, tipagem nativa, pattern matching e modularidade.
    """

    termometros: List["Termometro"] = field(init=False)
    painel_controle: "PainelControle" = field(init=False)
    materiais_display: List["MaterialDisplay"] = field(init=False)
    _font_cache: ClassVar[dict] = {}

    def __post_init__(self) -> None:
        """Inicializa os componentes da interface após a criação da instância."""
        # Inicialização dos termômetros para cada escala
        self.termometros = [
            Termometro(TERMOMETRO_XS[0], TemperatureScale.KELVIN),
            Termometro(TERMOMETRO_XS[1], TemperatureScale.CELSIUS),
            Termometro(TERMOMETRO_XS[2], TemperatureScale.FAHRENHEIT),
        ]
        # Inicialização do painel de controle
        self.painel_controle = PainelControle(
            rect=(PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H)
        )
        # Inicialização dos displays de materiais usando enums
        self.materiais_display = [
            MaterialDisplay(MATERIAL_XS[i], material_type)
            for i, material_type in enumerate(MaterialType)
        ]

    def handle_event(self, event: pygame.event.Event, state: "AppState") -> "AppState":
        """
        Processa um evento PyGame e retorna o novo estado da aplicação.
        Utiliza delegação funcional para cada componente.
        """
        novo_state = state
        # Delegação funcional: cada termômetro pode atualizar o estado
        for termo in self.termometros:
            resultado = termo.handle_event(event, novo_state)
            if resultado is not None and resultado != novo_state:
                novo_state = resultado
        # O painel de controle pode atualizar o estado
        novo_state = self.painel_controle.handle_event(event, novo_state)
        return novo_state

    def render(self, surface: pygame.Surface, state: "AppState") -> None:
        """
        Renderiza todos os componentes da interface na superfície fornecida.
        """
        # Renderização dos termômetros
        for termo in self.termometros:
            termo.render(surface, state)
        # Renderização do painel de controle
        self.painel_controle.render(surface, state)
        # Renderização dos displays de materiais
        temp_celsius = state.valores()[TemperatureScale.CELSIUS]
        font = self._get_font("rotulo")
        for i, material in enumerate(self.materiais_display):
            material.render(
                surface,
                temp_celsius,
                font=font,
                label_color=CORES["texto"],
                border_color=CORES["material_borda"],
            )

    @classmethod
    def _get_font(cls, name: str) -> pygame.font.Font:
        """
        Retorna uma fonte do cache ou carrega se necessário.
        """
        if name in cls._font_cache:
            return cls._font_cache[name]
        # Exemplo: mapeamento de fontes por nome
        font_map = {
            "rotulo": ("Arial", 24, False),
            "titulo": ("Arial", 32, True),
            "valor": ("Arial", 28, True),
        }
        family, size, bold = font_map.get(name, ("Arial", 24, False))
        font = pygame.font.SysFont(family, size, bold=bold)
        cls._font_cache[name] = font
        return font
