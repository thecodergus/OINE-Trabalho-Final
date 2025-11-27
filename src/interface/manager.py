import pygame
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
from src.components.material_display import MaterialDisplay
from src.core.state import AppState
from src.temperature_types import TemperatureScale


class InterfaceManager:
    def __init__(self) -> None:
        self.termometros = [
            Termometro(TERMOMETRO_XS[0], TemperatureScale.KELVIN),
            Termometro(TERMOMETRO_XS[1], TemperatureScale.CELSIUS),
            Termometro(TERMOMETRO_XS[2], TemperatureScale.FAHRENHEIT),
        ]
        self.painel_controle = PainelControle(
            rect=(PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H)
        )
        self.materiais_display = []
        for i in range(len(MATERIAIS)):
            nome, img_path = MATERIAIS[i]
            print(f"Criando MaterialDisplay {i}: nome={nome}, img_path={img_path}")
            self.materiais_display.append(MaterialDisplay(MATERIAL_XS[i], nome, img_path))

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        novo_state = state
        for termo in self.termometros:
            resultado = termo.handle_event(event, novo_state)
            if resultado is not None and resultado != novo_state:
                novo_state = resultado
        # Sempre passa o evento para o painel de controle, com o estado atualizado
        return self.painel_controle.handle_event(event, novo_state)

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        for termo in self.termometros:
            termo.render(surface, state)
        self.painel_controle.render(surface, state)
        for material in self.materiais_display:
            material.render(surface, state)
