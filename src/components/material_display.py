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
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {img_path}")
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.w, self.h))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar imagem {img_path}: {e}")
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
