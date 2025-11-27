import pygame
import os
from ..config.settings import (
    MATERIAL_IMG_Y,
    MATERIAL_IMG_DIM,
    CORES,
    MATERIAL_LABEL_Y,
    FONTES,
)
from ..core.state import AppState


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
        pygame.draw.rect(
            image,
            CORES["material_fundo"],
            (0, 0, self.w, self.h),
            border_radius=8,
        )
        pygame.draw.line(
            image, CORES["material_borda"], (0, 0), (self.w, self.h), 2
        )
        pygame.draw.line(
            image, CORES["material_borda"], (self.w, 0), (0, self.h), 2
        )
        return image

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o display do material."""
        self._render_label(surf)
        self._render_image(surf)
        self._render_border(surf)

    def _render_label(self, surf: pygame.Surface) -> None:
        """Renderiza o rótulo do material."""
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(self.nome, True, CORES["texto"])
        surf.blit(txt, (self.x + (self.w - txt.get_width()) // 2, MATERIAL_LABEL_Y))

    def _render_image(self, surf: pygame.Surface) -> None:
        """Renderiza a imagem do material."""
        surf.blit(self.image, self.rect)

    def _render_border(self, surf: pygame.Surface) -> None:
        """Renderiza a borda ao redor da imagem do material."""
        pygame.draw.rect(surf, CORES["material_borda"], self.rect, 2, border_radius=8)
