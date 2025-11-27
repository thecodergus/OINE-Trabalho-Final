from dataclasses import dataclass
from typing import Optional, Dict
from src.config.settings import STRINGS
from src.utils.temperature_converter import celsius_to_kelvin, celsius_to_fahrenheit, kelvin_to_celsius, fahrenheit_to_celsius

@dataclass(frozen=True, slots=True)
class AppState:
    temp_min: float = -50.0
    temp_max: float = 300.0
    escala_ativa: str = STRINGS["escalas"]["celsius"]
    valor_ativo: float = 20.0
    arrastando: Optional[str] = None
    botao_mais_pressionado: bool = False
    botao_menos_pressionado: bool = False

    def valores(self) -> Dict[str, float]:
        """Calcula os valores equivalentes nas três escalas."""
        if self.escala_ativa == STRINGS["escalas"]["celsius"]:
            return self._valores_desde_celsius(self.valor_ativo)
        elif self.escala_ativa == STRINGS["escalas"]["kelvin"]:
            celsius = kelvin_to_celsius(self.valor_ativo)
            return self._valores_desde_celsius(celsius)
        elif self.escala_ativa == STRINGS["escalas"]["fahrenheit"]:
            celsius = fahrenheit_to_celsius(self.valor_ativo)
            return self._valores_desde_celsius(celsius)
        else:
            raise ValueError("Escala ativa inválida")

    def _valores_desde_celsius(self, celsius: float) -> Dict[str, float]:
        """Calcula os valores equivalentes a partir de Celsius."""
        return {
            STRINGS["escalas"]["celsius"]: celsius,
            STRINGS["escalas"]["kelvin"]: celsius_to_kelvin(celsius),
            STRINGS["escalas"]["fahrenheit"]: celsius_to_fahrenheit(celsius),
        }

    def clamp_valor(self, valor: float) -> float:
        return max(self.temp_min, min(self.temp_max, valor))
    
    def atinge_limite_maximo(self) -> bool:
        """Verifica se algum dos valores atingiu o limite máximo."""
        valores = self.valores()
        # Verifica se qualquer escala atingiu seu limite máximo real (não os limites configurados)
        # Zero absoluto em Kelvin é 0K, e o limite superior é arbitrário mas deve ser respeitado
        return (valores[STRINGS["escalas"]["celsius"]] >= self.temp_max or
                valores[STRINGS["escalas"]["kelvin"]] >= celsius_to_kelvin(self.temp_max) or
                valores[STRINGS["escalas"]["fahrenheit"]] >= celsius_to_fahrenheit(self.temp_max))
    
    def atinge_limite_minimo(self) -> bool:
        """Verifica se algum dos valores atingiu o limite mínimo."""
        valores = self.valores()
        # Verifica se qualquer escala atingiu seu limite mínimo real
        return (valores[STRINGS["escalas"]["celsius"]] <= self.temp_min or
                valores[STRINGS["escalas"]["kelvin"]] <= celsius_to_kelvin(self.temp_min) or
                valores[STRINGS["escalas"]["fahrenheit"]] <= celsius_to_fahrenheit(self.temp_min))
