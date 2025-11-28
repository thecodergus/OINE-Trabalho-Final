from enum import Enum, auto
from typing import ClassVar, Dict, Tuple, Optional
import pygame
import os

from utils.load_images import resource_path


class MaterialType(Enum):
    """Enumeração para tipos de materiais."""

    AGUA = auto()
    VIDRO = auto()
    ALUMINIO = auto()


class MaterialState(Enum):
    """Enumeração para estados dos materiais."""

    SOLIDO = auto()
    LIQUIDO = auto()
    GASOSO = auto()


class MaterialDisplay:
    """
    Exibe um material com imagem e rótulo, atualizando visualmente conforme a temperatura.
    - Uso rigoroso dos enums MaterialType e MaterialState.
    - Tipagem moderna, funções puras, cache de imagens, robustez e performance.
    - Compatível com Python 3.13+ e PyGame 2.6.
    """

    _image_cache: ClassVar[Dict[Tuple[MaterialType, MaterialState], pygame.Surface]] = (
        {}
    )
    _placeholder: ClassVar[Optional[pygame.Surface]] = None

    def __init__(self, x: int, material_type: MaterialType) -> None:
        self.x: int = x
        self.y: int = 500
        self.w: int = 200
        self.h: int = 200
        self.material_type: MaterialType = material_type
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self._current_state: Optional[MaterialState] = None
        self._current_image: Optional[pygame.Surface] = None

    @staticmethod
    def _state_for_temperature(
        material_type: MaterialType, temp_celsius: float
    ) -> MaterialState:
        """
        Função pura: determina o estado físico do material para uma dada temperatura.
        """
        match material_type:
            case MaterialType.AGUA:
                if temp_celsius < 0.0:
                    return MaterialState.SOLIDO
                elif temp_celsius < 100.0:
                    return MaterialState.LIQUIDO
                else:
                    return MaterialState.GASOSO
            case MaterialType.VIDRO:
                if temp_celsius < 1000.0:
                    return MaterialState.SOLIDO
                elif temp_celsius < 1500.0:
                    return MaterialState.LIQUIDO
                else:
                    return MaterialState.GASOSO
            case MaterialType.ALUMINIO:
                if temp_celsius < 660.0:
                    return MaterialState.SOLIDO
                elif temp_celsius < 2500.0:
                    return MaterialState.LIQUIDO
                else:
                    return MaterialState.GASOSO
            case _:
                return MaterialState.SOLIDO  # fallback seguro

    @staticmethod
    def _img_path(material_type: MaterialType, state: MaterialState) -> str:
        """
        Função pura: retorna o caminho RELATIVO da imagem para o material e estado.
        Corrigido: retorna sempre a partir de 'assets/', nunca inclui 'src/'.
        """
        base = "assets"
        match material_type, state:
            case MaterialType.AGUA, MaterialState.SOLIDO:
                return f"{base}/Agua-solido.png"
            case MaterialType.AGUA, MaterialState.LIQUIDO:
                return f"{base}/Agua-liquida.png"
            case MaterialType.AGUA, MaterialState.GASOSO:
                return f"{base}/Agua-gasosa.png"
            case MaterialType.VIDRO, MaterialState.SOLIDO:
                return f"{base}/Vidro-solido.png"
            case MaterialType.VIDRO, MaterialState.LIQUIDO:
                return f"{base}/Vidro-liquida.png"
            case MaterialType.VIDRO, MaterialState.GASOSO:
                return f"{base}/Vidro-gasosa.png"
            case MaterialType.ALUMINIO, MaterialState.SOLIDO:
                return f"{base}/Aluminio-solido.png"
            case MaterialType.ALUMINIO, MaterialState.LIQUIDO:
                return f"{base}/Aluminio-liquida.png"
            case MaterialType.ALUMINIO, MaterialState.GASOSO:
                return f"{base}/Aluminio-gasosa.png"
            case _:
                return f"{base}/imagem_generica.jpg"

    @classmethod
    def _get_placeholder(cls, w: int, h: int) -> pygame.Surface:
        """
        Gera ou retorna o placeholder único para imagens ausentes.
        """
        if cls._placeholder is not None:
            return cls._placeholder
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((255, 0, 0, 128))
        pygame.draw.rect(surf, (255, 255, 255, 255), (0, 0, w, h), 3)
        pygame.draw.line(surf, (255, 255, 255, 255), (5, 5), (w - 5, h - 5), 3)
        pygame.draw.line(surf, (255, 255, 255, 255), (w - 5, 5), (5, h - 5), 3)
        try:
            font = pygame.font.SysFont(None, 20)
            text = font.render("NO IMG", True, (255, 255, 255, 255))
            text_rect = text.get_rect(center=(w // 2, h // 2))
            surf.blit(text, text_rect)
        except Exception:
            pass
        cls._placeholder = surf
        return surf

    @classmethod
    def _load_image(cls, material_type, state, w: int, h: int) -> pygame.Surface:
        """
        Carrega e converte a imagem, usando cache. Fallback para placeholder.
        """
        key = (material_type, state)
        if key in cls._image_cache:
            return cls._image_cache[key]
        nome_arquivo = cls._img_path(material_type, state)  # Ex: 'Agua-solido.png'
        caminho = resource_path(f"assets/{nome_arquivo}")
        try:
            if not os.path.exists(caminho):
                raise FileNotFoundError(f"Imagem não encontrada: {caminho}")
            img = pygame.image.load(caminho).convert_alpha()
            img = pygame.transform.scale(img, (w, h))
            cls._image_cache[key] = img
            return img
        except Exception as e:
            print(f"[MaterialDisplay] Falha ao carregar '{caminho}': {e}")
            placeholder = cls._get_placeholder(w, h)
            cls._image_cache[key] = placeholder
            return placeholder

    def update_image(self, temp_celsius: float) -> None:
        """
        Atualiza a imagem apenas se o estado mudou.
        """
        state = self._state_for_temperature(self.material_type, temp_celsius)
        if state != self._current_state:
            self._current_image = self._load_image(
                self.material_type, state, self.w, self.h
            )
            self._current_state = state

    def render(
        self,
        surf: pygame.Surface,
        temp_celsius: float,
        font: pygame.font.Font,
        label_color: tuple[int, int, int] = (0, 0, 0),
        border_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """
        Renderiza o material: imagem, rótulo e borda.
        """
        self.update_image(temp_celsius)
        surf.blit(self._current_image, self.rect)  # type: ignore
        label = font.render(self.material_type.name.capitalize(), True, label_color)
        label_x = self.x + (self.w - label.get_width()) // 2
        label_y = self.y + self.h + 10
        surf.blit(label, (label_x, label_y))
