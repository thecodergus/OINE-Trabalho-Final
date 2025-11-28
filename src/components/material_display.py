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
        # Define state mappings for materials based on melting/boiling points
        self.state_mapping = self._get_state_mapping()
        self.image = self._load_image(img_path)

    def _get_state_mapping(self) -> dict:
        """Define melting and boiling points for materials to determine states."""
        # Standard material points in Celsius
        # These values are approximated for educational purposes
        if self.nome == "Água":
            return {
                "solid": -0.1,  # Water freezes at 0°C
                "liquid": 0.1,  # Water melts at 0°C (min liquid)
                "gas": 100.0,  # Water boils at 100°C (gas state)
            }
        elif self.nome == "Vidro":
            return {
                "solid": 1000.0,  # Approximate melting point of glass
                "liquid": 1500.0,  # Approximate melting point
                "gas": float("inf"),  # No boiling in typical conditions
            }
        elif self.nome == "Alumínio":
            return {
                "solid": 660.0,  # Aluminum melting point
                "liquid": 661.0,  # Aluminum melting (min liquid)
                "gas": 2500.0,  # Aluminum boiling point
            }
        else:
            return {
                "solid": float("-inf"),
                "liquid": float("-inf"),
                "gas": float("inf"),
            }

    def _load_image(self, img_path: str) -> pygame.Surface:
        """Carrega e prepara a imagem do material."""
        try:
            # Try the path as-is first
            if os.path.exists(img_path):
                image = pygame.image.load(img_path).convert_alpha()
                return pygame.transform.scale(image, (self.w, self.h))

            # If that fails, try relative to project root
            # Get the project root (assuming this file is in src/components)
            project_root = os.path.join(os.path.dirname(__file__), "..", "..")
            full_path = os.path.join(project_root, img_path)
            full_path = os.path.normpath(full_path)

            if os.path.exists(full_path):
                image = pygame.image.load(full_path).convert_alpha()
                return pygame.transform.scale(image, (self.w, self.h))

            raise FileNotFoundError(
                f"Arquivo não encontrado: {img_path} ou {full_path}"
            )
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

    def _update_image_based_on_temperature(self, state: AppState) -> None:
        """Atualiza a imagem do material baseada no estado atual."""
        # Get the active temperature value (in Celsius)
        active_temp_celsius = state.valor_ativo

        # Based on the material type and current temperature, select appropriate image
        if self.nome == "Água":
            # Get water state (solid, liquid, gas) based on temperature
            if active_temp_celsius <= self.state_mapping["solid"]:
                # Solid state - ice
                try:
                    new_image = self._load_image("src/assets/Agua-solido.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, default to liquid for demonstration
                    pass
            elif active_temp_celsius <= self.state_mapping["gas"]:
                # Liquid state - water
                try:
                    new_image = self._load_image("src/assets/Agua-liquida.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, stay with current image
                    pass
            else:
                # Gas state - steam
                try:
                    new_image = self._load_image("src/assets/Agua-gasosa.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, default to liquid for demonstration
                    pass

        elif self.nome == "Vidro":
            # For glass, decide based on temperature
            if active_temp_celsius < self.state_mapping["solid"]:
                # Solid state - regular glass
                try:
                    new_image = self._load_image("src/assets/Vidro-solido.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass
            elif active_temp_celsius < self.state_mapping["gas"]:
                # Liquid state (molten glass)
                try:
                    new_image = self._load_image("src/assets/Vidro-liquida.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass
            else:
                # Gas state (very high temperature)
                try:
                    new_image = self._load_image("src/assets/Vidro-gasosa.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass

        elif self.nome == "Alumínio":
            # For aluminum, decide based on temperature
            if active_temp_celsius < self.state_mapping["solid"]:
                # Solid state - solid aluminum
                try:
                    new_image = self._load_image("src/assets/Aluminio-solido.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass
            elif active_temp_celsius < self.state_mapping["gas"]:
                # Liquid state (molten aluminum)
                try:
                    new_image = self._load_image("src/assets/Aluminio-liquida.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass
            else:
                # Gas state (very high temperature)
                try:
                    new_image = self._load_image("src/assets/Aluminio-gasosa.png")
                    if new_image is not None:
                        self.image = new_image
                except:
                    # If image not available, keep original for demo
                    pass

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        """Renderiza o display do material."""
        # Update image based on current temperature
        self._update_image_based_on_temperature(state)
        self._render_label(surf, state)
        self._render_image(surf)
        self._render_border(surf)

    def _render_label(self, surf: pygame.Surface, state: AppState) -> None:
        # Mostrar o nome do material em vez do intervalo de temperatura
        fonte = get_font_by_name("rotulo")
        txt = fonte.render(
            self.nome,
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
