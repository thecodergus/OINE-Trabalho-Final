from enum import Enum
from typing import Dict, Tuple


class TemperatureScale(Enum):
    """Enumeração que representa as diferentes escalas de temperatura."""
    
    CELSIUS = "celsius"
    KELVIN = "kelvin"
    FAHRENHEIT = "fahrenheit"
    
    @property
    def symbol(self) -> str:
        """Retorna o símbolo da escala de temperatura."""
        symbols = {
            TemperatureScale.CELSIUS: "°C",
            TemperatureScale.KELVIN: "K",
            TemperatureScale.FAHRENHEIT: "°F",
        }
        return symbols[self]
    
    @property
    def name_display(self) -> str:
        """Retorna o nome formatado da escala de temperatura."""
        names = {
            TemperatureScale.CELSIUS: "Celsius",
            TemperatureScale.KELVIN: "Kelvin",
            TemperatureScale.FAHRENHEIT: "Fahrenheit",
        }
        return names[self]
    
    @property
    def absolute_zero(self) -> float:
        """Retorna o valor do zero absoluto na escala."""
        zeros = {
            TemperatureScale.CELSIUS: -273.15,
            TemperatureScale.KELVIN: 0.0,
            TemperatureScale.FAHRENHEIT: -459.67,
        }
        return zeros[self]
    
    @classmethod
    def from_symbol(cls, symbol: str) -> 'TemperatureScale':
        """Cria uma instância de TemperatureScale a partir de um símbolo."""
        symbol_map = {
            "°C": cls.CELSIUS,
            "K": cls.KELVIN,
            "°F": cls.FAHRENHEIT,
        }
        return symbol_map.get(symbol, cls.CELSIUS)
    
    @classmethod
    def list_all(cls) -> Tuple['TemperatureScale', ...]:
        """Retorna uma tupla com todas as escalas disponíveis."""
        return (
            cls.CELSIUS,
            cls.KELVIN,
            cls.FAHRENHEIT
        )
    
    def __str__(self) -> str:
        """Retorna uma representação em string da escala."""
        return self.value
    
    def __repr__(self) -> str:
        """Retorna uma representação detalhada da escala."""
        return f"TemperatureScale.{self.name}"
