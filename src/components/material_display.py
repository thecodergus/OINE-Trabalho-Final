import pygame
import os

from ..config.constants import MATERIAL_LABEL_Y, BORDA_ARREDONDADA
from ..config.settings import (
    MATERIAL_IMG_Y,
    MATERIAL_IMG_DIM,
    CORES,
)
from ..core.state import AppState
from src.temperature_types import TemperatureScale
from ..utils.temperature_converter import converter
from ..utils.font_cache import get_font_by_name
from ..utils.render_utils import draw_rounded_rect_with_border


class MaterialDisplay:
    def __init__(self, x: int, nome: str, img_path: str) -> None:
        self.x = x
        self.y = MATERIAL_IMG_Y
        self.w, self.h = MATERIAL_IMG_DIM
        self.nome = nome
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.image = self._load_image(img_path)

    def _load_image(self, img_path: str) -> pygame.Surface:
        """Carrega e prepara a imagem do material."""
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {img_path}")
            image = pygame.image.load(img_path).convert_alpha()
            return pygame.transform.scale(image, (self.w, self.h))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar imagem {img_path}: {e}")
            return self._create_placeholder_image()

    def _create_placeholder_image(self) -> pygame.Surface:
        """Cria uma imagem placeholder quando a imagem original não pode ser carregada."""
        image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        image.fill((0, 0, 0, 0))
        draw_rounded_rect_with_border(
            image,
            pygame.Rect(0, 0, self.w, self.h),
            CORES["material_fundo"],
            CORES["material_fundo"],  # Same color for border since we want solid fill
            0,  # No border
            BORDA_ARREDONDADA,  # Border radius
        )
        pygame.draw.line(image, CORES["material_borda"], (0, 0), (self.w, self.h), 2)
        pygame.draw.line(image, CORES["material_borda"], (self.w, 0), (0, self.h), 2)
        return image

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o display do material."""
        self._render_label(surf, state)
        self._render_image(surf)
        self._render_border(surf)

    def _render_label(self, surf: pygame.Surface, state: AppState) -> None:
        # Converta os valores conforme a escala ativa
        min_convertido = converter(
            state.temp_min, TemperatureScale.CELSIUS, state.escala_ativa
        )
        max_convertido = converter(
            state.temp_max, TemperatureScale.CELSIUS, state.escala_ativa
        )
        fonte = get_font_by_name("rotulo")
        txt = fonte.render(
            f"({int(min_convertido)}, {int(max_convertido)}) {state.escala_ativa.symbol}",
            True,
            CORES["texto"],
        )
        # Position label centered below each material image
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, MATERIAL_LABEL_Y))

    def _render_image(self, surf: pygame.Surface) -> None:
        """Renderiza a imagem do material."""
        surf.blit(self.image, self.rect)

    def _render_border(self, surf: pygame.Surface) -> None:
        """Renderiza a borda ao redor da imagem do material."""
        draw_rounded_rect_with_border(
            surf, self.rect, (0, 0, 0, 0), CORES["material_borda"], 2, 8
        )
