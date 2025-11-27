import pygame
from dataclasses import dataclass, replace
from typing import Tuple, Optional, Literal, Dict

# =========================
# 1. Utilitários e Constantes
# =========================


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Formato hexadecimal inválido: '{h}'")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


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

# Fontes dobradas
FONTES = {
    "titulo": ("Arial", 32, True),  # Dobro do padrão anterior
    "rotulo": ("Arial", 24, False),
    "valor": ("Arial", 28, True),
}

TELA_LARGURA, TELA_ALTURA = 1024, 768

# Termômetros
TERMOMETRO_DIM = (32, 293)
TERMOMETRO_Y = 111
TERMOMETRO_COUNT = 3
TERMOMETRO_ESCALAS = ["K", "°C", "°F"]
THUMB_RAIO = 18
BASE_RAIO = 22


# Espaçamento dinâmico centralizado
def calcular_termometro_xs() -> Tuple[int, int, int]:
    margem_lateral = 159
    area_util = TELA_LARGURA - 2 * margem_lateral
    espacamento = (area_util - TERMOMETRO_COUNT * TERMOMETRO_DIM[0]) // (
        TERMOMETRO_COUNT - 1
    )
    xs = [
        margem_lateral + i * (TERMOMETRO_DIM[0] + espacamento)
        for i in range(TERMOMETRO_COUNT)
    ]
    # Convertendo explicitamente para Tuple[int, int, int] para satisfazer o type hint
    return (xs[0], xs[1], xs[2])


TERMOMETRO_XS = calcular_termometro_xs()

# Painel lateral direito
PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H = 860, 77, 120, 180
BOTAO_RAIO = 18
BOTAO_Y = PAINEL_Y + 60
BOTAO_MAIS_X = PAINEL_X + 80
BOTAO_MENOS_X = PAINEL_X + 22
FAIXA_LABEL_Y = PAINEL_Y + 20

# Materiais (parte inferior)
MATERIAL_IMG_DIM = (120, 88)
MATERIAL_IMG_Y = 549
MATERIAL_LABEL_Y = MATERIAL_IMG_Y - 48  # Ajustado para fonte maior
MATERIAL_XS = [159, 444, 717]
MATERIAIS = [
    ("Água", "src/assets/imagem_generica.jpg"),
    ("Vidro", "src/assets/imagem_generica.jpg"),
    ("Alumínio", "src/assets/imagem_generica.jpg"),
]

# =========================
# 2. Conversão de Temperaturas
# =========================


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
    if de == "°C":
        if para == "K":
            return celsius_to_kelvin(valor)
        if para == "°F":
            return celsius_to_fahrenheit(valor)
    if de == "K":
        c = kelvin_to_celsius(valor)
        return c if para == "°C" else celsius_to_fahrenheit(c)
    if de == "°F":
        c = fahrenheit_to_celsius(valor)
        return c if para == "°C" else celsius_to_kelvin(c)
    raise ValueError(f"Conversão inválida: {de} -> {para}")


# =========================
# 3. Estado Global Imutável
# =========================


@dataclass(frozen=True, slots=True)
class AppState:
    temp_min: float = -50.0
    temp_max: float = 300.0
    escala_ativa: str = "°C"  # "K", "°C", "°F"
    valor_ativo: float = 20.0
    arrastando: Optional[str] = None  # "K", "°C", "°F" ou None

    def valores(self) -> Dict[str, float]:
        match self.escala_ativa:
            case "°C":
                c = self.valor_ativo
                return {
                    "°C": c,
                    "K": celsius_to_kelvin(c),
                    "°F": celsius_to_fahrenheit(c),
                }
            case "K":
                k = self.valor_ativo
                c = kelvin_to_celsius(k)
                return {
                    "K": k,
                    "°C": c,
                    "°F": celsius_to_fahrenheit(c),
                }
            case "°F":
                f = self.valor_ativo
                c = fahrenheit_to_celsius(f)
                return {
                    "°F": f,
                    "°C": c,
                    "K": celsius_to_kelvin(c),
                }
            case _:
                raise ValueError("Escala ativa inválida")

    def clamp_valor(self, valor: float) -> float:
        return max(self.temp_min, min(self.temp_max, valor))


# =========================
# 4. Termômetro Interativo
# =========================


class Termometro:
    """
    Termômetro vertical com thumb arrastável e círculo na base, ambos vermelhos.
    """

    def __init__(self, x: int, escala: str) -> None:
        self.x = x
        self.y = TERMOMETRO_Y
        self.w, self.h = TERMOMETRO_DIM
        self.escala = escala
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def valor_para_y(self, valor: float, temp_min: float, temp_max: float) -> int:
        ratio = (valor - temp_min) / (temp_max - temp_min)
        return int(self.y + self.h - ratio * self.h)

    def y_para_valor(self, y: int, temp_min: float, temp_max: float) -> float:
        y = max(self.y, min(self.y + self.h, y))
        ratio = (self.y + self.h - y) / self.h
        return temp_min + ratio * (temp_max - temp_min)

    def thumb_pos(self, state: AppState) -> Tuple[int, int]:
        valor = state.valores()[self.escala]
        y = self.valor_para_y(valor, state.temp_min, state.temp_max)
        x = self.x + self.w // 2
        return (x, y)

    def base_pos(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h)

    def handle_event(
        self, event: pygame.event.Event, state: AppState
    ) -> Optional[AppState]:
        thumb_x, thumb_y = self.thumb_pos(state)
        mouse_x, mouse_y = getattr(event, "pos", (None, None))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                mouse_x is not None
                and mouse_y is not None
                and (thumb_x - THUMB_RAIO) <= mouse_x <= (thumb_x + THUMB_RAIO)
                and (thumb_y - THUMB_RAIO) <= mouse_y <= (thumb_y + THUMB_RAIO)
            ):
                return replace(state, arrastando=self.escala)
        elif event.type == pygame.MOUSEBUTTONUP:
            if state.arrastando == self.escala:
                return replace(state, arrastando=None)
        elif event.type == pygame.MOUSEMOTION:
            if state.arrastando == self.escala and mouse_y is not None:
                novo_valor = self.y_para_valor(mouse_y, state.temp_min, state.temp_max)
                novo_valor = state.clamp_valor(novo_valor)
                return AppState(
                    temp_min=state.temp_min,
                    temp_max=state.temp_max,
                    escala_ativa=self.escala,
                    valor_ativo=novo_valor,
                    arrastando=self.escala,
                )
        return None

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Corpo do termômetro
        pygame.draw.rect(surf, (240, 240, 240), self.rect, border_radius=8)
        pygame.draw.rect(surf, CORES["termometro_borda"], self.rect, 2, border_radius=8)
        # Nível preenchido
        valor = state.valores()[self.escala]
        nivel = (valor - state.temp_min) / (state.temp_max - state.temp_min)
        nivel_px = int(self.h * nivel)
        rect_preenchido = pygame.Rect(
            self.x, self.y + self.h - nivel_px, self.w, nivel_px
        )
        pygame.draw.rect(surf, CORES["indicador"], rect_preenchido, border_radius=8)
        # Círculo da base (vermelho)
        base_x, base_y = self.base_pos()
        pygame.draw.circle(surf, CORES["indicador"], (base_x, base_y), BASE_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (base_x, base_y), BASE_RAIO, 2)
        # Thumb (bolinha vermelha)
        thumb_x, thumb_y = self.thumb_pos(state)
        pygame.draw.circle(surf, CORES["indicador"], (thumb_x, thumb_y), THUMB_RAIO)
        pygame.draw.circle(surf, CORES["texto"], (thumb_x, thumb_y), THUMB_RAIO, 2)
        # Label acima
        fonte = pygame.font.SysFont(*FONTES["valor"])
        txt = fonte.render(f"{valor:.2f} {self.escala}", True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, self.y - 48))


# =========================
# 5. Painel de Controle (Intervalo)
# =========================


class PainelControle:
    """
    Painel de controle: botões + e -, exibe intervalo dinâmico.
    """

    def __init__(self, rect: Tuple[int, int, int, int]) -> None:
        self.panel_rect = pygame.Rect(rect)
        self.botao_mais = pygame.Rect(
            BOTAO_MAIS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )
        self.botao_menos = pygame.Rect(
            BOTAO_MENOS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )
        self.min_intervalo = 10.0

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        if state.arrastando is not None:
            return state
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_mais.collidepoint(event.pos):
                novo_max = state.temp_max + 10
                if novo_max - state.temp_min >= self.min_intervalo:
                    novo_valor = min(state.valor_ativo, novo_max)
                    return replace(state, temp_max=novo_max, valor_ativo=novo_valor)
            if self.botao_menos.collidepoint(event.pos):
                novo_min = state.temp_min - 10
                if state.temp_max - novo_min >= self.min_intervalo:
                    novo_valor = max(state.valor_ativo, novo_min)
                    return replace(state, temp_min=novo_min, valor_ativo=novo_valor)
        return state

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        pygame.draw.rect(
            surf,
            CORES["painel"],
            (PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H),
            border_radius=16,
        )
        pygame.draw.rect(
            surf,
            CORES["painel_borda"],
            (PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H),
            2,
            border_radius=16,
        )
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(
            f"({int(state.temp_min)}, {int(state.temp_max)}) ºC", True, CORES["texto"]
        )
        surf.blit(txt, (PAINEL_X + (PAINEL_W - txt.get_width()) // 2, FAIXA_LABEL_Y))
        # Botão +
        pygame.draw.circle(
            surf, CORES["botao_mais"], self.botao_mais.center, BOTAO_RAIO
        )
        pygame.draw.circle(surf, CORES["texto"], self.botao_mais.center, BOTAO_RAIO, 2)
        fonte_b = pygame.font.SysFont(*FONTES["titulo"])
        txt_mais = fonte_b.render("+", True, CORES["texto"])
        surf.blit(
            txt_mais,
            (
                self.botao_mais.centerx - txt_mais.get_width() // 2,
                self.botao_mais.centery - txt_mais.get_height() // 2,
            ),
        )
        # Botão -
        pygame.draw.circle(
            surf, CORES["botao_menos"], self.botao_menos.center, BOTAO_RAIO
        )
        pygame.draw.circle(surf, CORES["texto"], self.botao_menos.center, BOTAO_RAIO, 2)
        txt_menos = fonte_b.render("−", True, CORES["texto"])
        surf.blit(
            txt_menos,
            (
                self.botao_menos.centerx - txt_menos.get_width() // 2,
                self.botao_menos.centery - txt_menos.get_height() // 2,
            ),
        )


# =========================
# 6. Imagens dos Materiais
# =========================


class MaterialDisplay:
    """
    Exibe imagem do material e nome acima.
    """

    def __init__(self, x: int, nome: str, img_path: str) -> None:
        self.x = x
        self.y = MATERIAL_IMG_Y
        self.w, self.h = MATERIAL_IMG_DIM
        self.nome = nome
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        try:
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        except Exception:
            self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
            pygame.draw.rect(
                self.image,
                CORES["material_fundo"],
                (0, 0, self.w, self.h),
                border_radius=8,
            )
            pygame.draw.line(
                self.image, CORES["material_borda"], (0, 0), (self.w, self.h), 2
            )
            pygame.draw.line(
                self.image, CORES["material_borda"], (self.w, 0), (0, self.h), 2
            )

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(self.nome, True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, MATERIAL_LABEL_Y))
        surf.blit(self.image, self.rect)
        pygame.draw.rect(surf, CORES["material_borda"], self.rect, 2, border_radius=8)


# =========================
# 7. Interface Principal
# =========================


class InterfaceManager:
    """
    Gerencia todos os componentes da interface.
    """

    def __init__(self) -> None:
        self.termometros = [
            Termometro(TERMOMETRO_XS[0], "K"),
            Termometro(TERMOMETRO_XS[1], "°C"),
            Termometro(TERMOMETRO_XS[2], "°F"),
        ]
        self.painel_controle = PainelControle(
            rect=(PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H)
        )
        self.materiais_display = [
            MaterialDisplay(MATERIAL_XS[i], MATERIAIS[i][0], MATERIAIS[i][1])
            for i in range(len(MATERIAIS))
        ]

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        # Prioridade: arraste de termômetro > painel de controle
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


# =========================
# 8. Função Principal
# =========================


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


# =========================
# 9. Execução Direta
# =========================

if __name__ == "__main__":
    main()
