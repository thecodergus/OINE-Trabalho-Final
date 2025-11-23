# =============================================================================
# Codemagus — Simulação de Temperatura (Wireframe Fiel)
# Python 3.13+, PyGame 2.6+, arquitetura funcional, tipagem moderna
# =============================================================================

import pygame
from dataclasses import dataclass, replace
from typing import Tuple, Literal, List

# =============================================================================
# 1. Constantes de Layout e Aparência
# =============================================================================

TELA_LARGURA: int = 1024
TELA_ALTURA: int = 768

# Termômetros
TERMOMETRO_DIM: Tuple[int, int] = (32, 293)
TERMOMETRO_Y: int = 111
TERMOMETRO_XS: List[int] = [159, 502, 703]
TERMOMETRO_ESCALAS: List[Literal["K", "°C", "°F"]] = ["K", "°C", "°F"]

# Painel lateral direito
PAINEL_X: int = 860
PAINEL_Y: int = 77
PAINEL_W: int = 120
PAINEL_H: int = 180

# Botões + e -
BOTAO_RAIO: int = 18
BOTAO_Y: int = PAINEL_Y + 60
BOTAO_MAIS_X: int = PAINEL_X + 80
BOTAO_MENOS_X: int = PAINEL_X + 22

# Texto faixa temperatura
FAIXA_LABEL_Y: int = PAINEL_Y + 20

# Imagens dos materiais (parte inferior)
MATERIAL_IMG_DIM: Tuple[int, int] = (120, 88)
MATERIAL_IMG_Y: int = 549
MATERIAL_LABEL_Y: int = MATERIAL_IMG_Y - 32
MATERIAL_XS: List[int] = [159, 444, 717]
MATERIAIS: List[Tuple[str, str]] = [
    ("Água", "agua.png"),
    ("Vidro", "vidro.png"),
    ("Alumínio", "aluminio.png"),
]

# Cores
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Converte uma string hexadecimal (#RRGGBB ou RRGGBB) em uma tupla RGB (r, g, b).
    Garante tipagem Tuple[int, int, int] para compatibilidade com type checkers modernos.
    """
    h = hex_color.lstrip('#')
    if len(h) != 6:
        raise ValueError(f"Formato hexadecimal inválido: '{hex_color}'. Esperado: #RRGGBB ou RRGGBB")
    # Desempacotamento explícito para garantir Tuple[int, int, int]
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return (r, g, b)

CORES = {
    "fundo": hex_to_rgb("#FFFFFF"),
    "texto": hex_to_rgb("#000000"),
    "indicador": hex_to_rgb("#FF0000"),
    "painel": (230, 230, 230),
    "painel_borda": (180, 180, 180),
    "botao_mais": hex_to_rgb("#4CAF50"),
    "botao_menos": hex_to_rgb("#F44336"),
    "termometro_borda": (80, 80, 80),
    "material_borda": (120, 120, 120),
    "material_fundo": (200, 200, 200),
}

FONTES = {
    "titulo": ("Arial", 16, True),
    "rotulo": ("Arial", 12, False),
    "valor": ("Arial", 14, True),
}

TEMP_MIN: float = -50.0
TEMP_MAX: float = 300.0

# =============================================================================
# 2. Estado Global Imutável
# =============================================================================

@dataclass(frozen=True, slots=True)
class AppState:
    temperatura_c: float = -5.0

    @property
    def temperatura_k(self) -> float:
        return self.temperatura_c + 273.15

    @property
    def temperatura_f(self) -> float:
        return self.temperatura_c * 9.0 / 5.0 + 32.0

# =============================================================================
# 3. Termômetro Vertical Fiel ao Wireframe
# =============================================================================

class Termometro:
    """
    Termômetro vertical alinhado ao wireframe, com label acima.
    """
    def __init__(self, x: int, escala: Literal["K", "°C", "°F"]) -> None:
        self.x = x
        self.y = TERMOMETRO_Y
        self.w, self.h = TERMOMETRO_DIM
        self.escala = escala
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def valor(self, state: AppState) -> float:
        match self.escala:
            case "K": return state.temperatura_k
            case "°C": return state.temperatura_c
            case "°F": return state.temperatura_f
            case _: return 0.0

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Corpo do termômetro
        pygame.draw.rect(surf, (240, 240, 240), self.rect, border_radius=8)
        pygame.draw.rect(surf, CORES["termometro_borda"], self.rect, 2, border_radius=8)
        # Nível preenchido
        v = self.valor(state)
        vmin, vmax = {
            "K": (223.15, 573.15),
            "°C": (TEMP_MIN, TEMP_MAX),
            "°F": (TEMP_MIN * 9/5 + 32, TEMP_MAX * 9/5 + 32),
        }[self.escala]
        nivel = max(0.0, min(1.0, (v - vmin) / (vmax - vmin)))
        nivel_px = int(self.h * nivel)
        rect_preenchido = pygame.Rect(self.x, self.y + self.h - nivel_px, self.w, nivel_px)
        pygame.draw.rect(surf, CORES["indicador"], rect_preenchido, border_radius=8)
        # Label acima
        fonte = pygame.font.SysFont(*FONTES["valor"])
        txt = fonte.render(f"{self.valor(state):.2f} {self.escala}", True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, self.y - 32))

# =============================================================================
# 4. Painel Lateral Direito: Faixa, Botões + e -
# =============================================================================

class PainelControle:
    """
    Painel de controle principal da simulação de temperatura.
    Gerencia faixa de temperatura e botões + e −, fiel ao wireframe.
    """
    def __init__(self, rect: tuple[int, int, int, int]) -> None:
        self.panel_rect = pygame.Rect(rect)
        # Botões lado a lado, centralizados verticalmente
        self.botao_mais = pygame.Rect(BOTAO_MAIS_X - BOTAO_RAIO, BOTAO_Y - BOTAO_RAIO, BOTAO_RAIO*2, BOTAO_RAIO*2)
        self.botao_menos = pygame.Rect(BOTAO_MENOS_X - BOTAO_RAIO, BOTAO_Y - BOTAO_RAIO, BOTAO_RAIO*2, BOTAO_RAIO*2)

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_mais.collidepoint(event.pos):
                return replace(state, temperatura_c=min(state.temperatura_c + 1, TEMP_MAX))
            if self.botao_menos.collidepoint(event.pos):
                return replace(state, temperatura_c=max(state.temperatura_c - 1, TEMP_MIN))
        return state

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Painel de fundo
        pygame.draw.rect(surf, CORES["painel"], (PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H), border_radius=16)
        pygame.draw.rect(surf, CORES["painel_borda"], (PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H), 2, border_radius=16)
        # Texto faixa temperatura (acima dos botões)
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render("(-50, 300) °C", True, CORES["texto"])
        surf.blit(txt, (PAINEL_X + (PAINEL_W - txt.get_width()) // 2, FAIXA_LABEL_Y))
        # Botão +
        pygame.draw.circle(surf, CORES["botao_mais"], self.botao_mais.center, BOTAO_RAIO)
        pygame.draw.circle(surf, CORES["texto"], self.botao_mais.center, BOTAO_RAIO, 2)
        fonte_b = pygame.font.SysFont(*FONTES["titulo"])
        txt_mais = fonte_b.render("+", True, CORES["texto"])
        surf.blit(txt_mais, (self.botao_mais.centerx - txt_mais.get_width()//2, self.botao_mais.centery - txt_mais.get_height()//2))
        # Botão -
        pygame.draw.circle(surf, CORES["botao_menos"], self.botao_menos.center, BOTAO_RAIO)
        pygame.draw.circle(surf, CORES["texto"], self.botao_menos.center, BOTAO_RAIO, 2)
        txt_menos = fonte_b.render("−", True, CORES["texto"])
        surf.blit(txt_menos, (self.botao_menos.centerx - txt_menos.get_width()//2, self.botao_menos.centery - txt_menos.get_height()//2))

# =============================================================================
# 5. Imagens dos Materiais (Parte Inferior)
# =============================================================================

class MaterialDisplay:
    """
    Exibe imagem do material e nome acima, fiel ao wireframe.
    """
    def __init__(self, x: int, nome: str, img_path: str) -> None:
        self.x = x
        self.y = MATERIAL_IMG_Y
        self.w, self.h = MATERIAL_IMG_DIM
        self.nome = nome
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        # Tenta carregar a imagem, se não conseguir, usa um placeholder
        try:
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        except Exception:
            self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.rect(self.image, CORES["material_fundo"], (0, 0, self.w, self.h), border_radius=8)
            pygame.draw.line(self.image, CORES["material_borda"], (0, 0), (self.w, self.h), 2)
            pygame.draw.line(self.image, CORES["material_borda"], (self.w, 0), (0, self.h), 2)

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Nome do material acima da imagem
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(self.nome, True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, MATERIAL_LABEL_Y))
        # Desenha a imagem (ou placeholder)
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, CORES["material_borda"], self.rect, 2, border_radius=8)

# =============================================================================
# 6. Gerenciador Principal da Interface
# =============================================================================

class InterfaceManager:
    """
    Gerencia todos os componentes da interface, garantindo layout fiel ao wireframe.
    """
    def __init__(self) -> None:
        self.termometros = [
            Termometro(TERMOMETRO_XS[0], TERMOMETRO_ESCALAS[0]),
            Termometro(TERMOMETRO_XS[1], TERMOMETRO_ESCALAS[1]),
            Termometro(TERMOMETRO_XS[2], TERMOMETRO_ESCALAS[2]),
        ]
        self.painel_controle = PainelControle(rect=(PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H))
        self.materiais_display = [
            MaterialDisplay(MATERIAL_XS[i], MATERIAIS[i][0], MATERIAIS[i][1])
            for i in range(len(MATERIAIS))
        ]

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        return self.painel_controle.handle_event(event, state)

    def render(self, surface: pygame.Surface, state: AppState) -> None:
        for termo in self.termometros:
            termo.render(surface, state)
        self.painel_controle.render(surface, state)
        for material in self.materiais_display:
            material.render(surface, state)

# =============================================================================
# 7. Função Principal (main loop)
# =============================================================================

def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Simulação de Temperatura")
    clock = pygame.time.Clock()
    interface = InterfaceManager()
    state = AppState()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                state = interface.handle_event(event, state)
        surface.fill(CORES["fundo"])
        interface.render(surface, state)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

# =============================================================================
# 8. Execução Direta
# =============================================================================

if __name__ == "__main__":
    main()

# =============================================================================
# Fim do código Codemagus — Simulação de Temperatura (Wireframe Fiel)
# =============================================================================
