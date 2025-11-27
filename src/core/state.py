from dataclasses import dataclass
from typing import Optional, Dict
from src.types import TemperatureScale
from src.config.settings import STRINGS
from src.utils.temperature_converter import (
    celsius_to_kelvin,
    celsius_to_fahrenheit,
    kelvin_to_celsius,
    fahrenheit_to_celsius,
)


@dataclass(frozen=True, slots=True)
class AppState:
    temp_min: float = -50.0
    temp_max: float = 50.0
    escala_ativa: TemperatureScale = TemperatureScale.CELSIUS
    valor_ativo: float = 20.0
    arrastando: Optional[str] = None
    botao_mais_pressionado: bool = False
    botao_menos_pressionado: bool = False

    def valores(self) -> Dict[TemperatureScale, float]:
        """Calcula os valores equivalentes nas três escalas."""
        if self.escala_ativa == TemperatureScale.CELSIUS:
            return self._valores_desde_celsius(self.valor_ativo)
        elif self.escala_ativa == TemperatureScale.KELVIN:
            celsius = kelvin_to_celsius(self.valor_ativo)
            return self._valores_desde_celsius(celsius)
        elif self.escala_ativa == TemperatureScale.FAHRENHEIT:
            celsius = fahrenheit_to_celsius(self.valor_ativo)
            return self._valores_desde_celsius(celsius)
        else:
            raise ValueError("Escala ativa inválida")

    def _valores_desde_celsius(self, celsius: float) -> Dict[TemperatureScale, float]:
        """Calcula os valores equivalentes a partir de Celsius."""
        return {
            TemperatureScale.CELSIUS: celsius,
            TemperatureScale.KELVIN: celsius_to_kelvin(celsius),
            TemperatureScale.FAHRENHEIT: celsius_to_fahrenheit(celsius),
        }

    def clamp_valor(self, valor: float) -> float:
        return max(self.temp_min, min(self.temp_max, valor))

    def atinge_limite_maximo(self) -> bool:
        """Verifica se algum dos valores atingiu o limite máximo."""
        valores = self.valores()
        # Verifica se qualquer escala atingiu seu limite máximo absoluto
        return (
            valores[TemperatureScale.CELSIUS] >= self.temp_max or
            valores[TemperatureScale.KELVIN] >= celsius_to_kelvin(self.temp_max) or
            valores[TemperatureScale.FAHRENHEIT] >= celsius_to_fahrenheit(self.temp_max)
        )

    def atinge_limite_minimo(self) -> bool:
        """Verifica se algum dos valores atingiu o limite mínimo."""
        valores = self.valores()
        # Verifica se qualquer escala atingiu seu limite mínimo absoluto
        return (
            valores[TemperatureScale.CELSIUS] <= self.temp_min or
            valores[TemperatureScale.KELVIN] <= celsius_to_kelvin(self.temp_min) or
            valores[TemperatureScale.FAHRENHEIT] <= celsius_to_fahrenheit(self.temp_min)
        )

    def pode_aumentar(self) -> bool:
        """Verifica se é possível aumentar a temperatura."""
        return not self.atinge_limite_maximo()

    def pode_diminuir(self) -> bool:
        """Verifica se é possível diminuir a temperatura."""
        return not self.atinge_limite_minimo()
