from typing import Dict
from ..temperature_types import TemperatureScale


def celsius_to_kelvin(c: float) -> float:
    return c + 273.15


def celsius_to_fahrenheit(c: float) -> float:
    return c * 9.0 / 5.0 + 32.0


def kelvin_to_celsius(k: float) -> float:
    return k - 273.15


def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32.0) * 5.0 / 9.0


def converter(valor: float, de: TemperatureScale, para: TemperatureScale) -> float:
    if de == para:
        return valor
    if de == TemperatureScale.CELSIUS:
        if para == TemperatureScale.KELVIN:
            return celsius_to_kelvin(valor)
        if para == TemperatureScale.FAHRENHEIT:
            return celsius_to_fahrenheit(valor)
    if de == TemperatureScale.KELVIN:
        c = kelvin_to_celsius(valor)
        return c if para == TemperatureScale.CELSIUS else celsius_to_fahrenheit(c)
    if de == TemperatureScale.FAHRENHEIT:
        c = fahrenheit_to_celsius(valor)
        return c if para == TemperatureScale.CELSIUS else celsius_to_kelvin(c)
    raise ValueError(f"Conversão inválida: {de} -> {para}")
