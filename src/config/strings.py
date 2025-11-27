"""Strings e textos da aplicação."""

from src.temperature_types import TemperatureScale

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
