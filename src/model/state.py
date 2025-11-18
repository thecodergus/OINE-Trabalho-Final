from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class AppState:
    """Estado imutável da aplicação (apenas valor do slider para o MVP)."""
    slider_value: float
