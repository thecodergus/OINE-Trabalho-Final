from typing import Dict
from ..config.settings import STRINGS


def celsius_to_kelvin(c: float) -> float:
    return c + 273.15


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0


def kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0


def converter(valor: float, de: str, para: str) -> float:
    if de == para:
        return valor
    if de == STRINGS["escalas"]["celsius"]:
        if para == STRINGS["escalas"]["kelvin"]:
            return celsius_to_kelvin(valor)
        if para == STRINGS["escalas"]["fahrenheit"]:
            return celsius_to_fahrenheit(valor)
    if de == STRINGS["escalas"]["kelvin"]:
        c = kelvin_to_celsius(valor)
        return c if para == STRINGS["escalas"]["celsius"] else celsius_to_fahrenheit(c)
    if de == STRINGS["escalas"]["fahrenheit"]:
        c = fahrenheit_to_celsius(valor)
        return c if para == STRINGS["escalas"]["celsius"] else celsius_to_kelvin(c)
    raise ValueError(f"Conversão inválida: {de} -> {para}")
