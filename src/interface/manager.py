import pygame
from src.config.settings import TERMOMETRO_XS, STRINGS, PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H, MATERIAL_XS, MATERIAIS
from src.components.thermometer import Termometro
from src.components.control_panel import PainelControle
from src.components.material_display import MaterialDisplay
from src.core.state import AppState

class InterfaceManager:
    def __init__(self) -> None:
        self.termometros = [
            Termometro(TERMOMETRO_XS[0], STRINGS["escalas"]["kelvin"]),
            Termometro(TERMOMETRO_XS[1], STRINGS["escalas"]["celsius"]),
            Termometro(TERMOMETRO_XS[2], STRINGS["escalas"]["fahrenheit"]),
        ]
        self.painel_controle = PainelControle(
            rect=(PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H)
        )
        self.materiais_display = [
            MaterialDisplay(MATERIAL_XS[i], MATERIAIS[i][0], MATERIAIS[i][1])
            for i in range(len(MATERIAIS))
        ]

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        for termo in self.termometros:
            novo = termo.handle_event(event, state)
            if novo is not None and novo != state:
                return novo
        return self.painel_controle.handle_event(event, state)

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        for termo in self.termometros:
            termo.render(surface, state)
        self.painel_controle.render(surface, state)
        for material in self.materiais_display:
            material.render(surface, state)
