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

# Enum for material types
from enum import Enum

class MaterialType(Enum):
    """Enumeração para tipos de materiais."""
    WATER = "Água"
    GLASS = "Vidro"
    ALUMINUM = "Alumínio"

# Enum for material states
class MaterialState(Enum):
    """Enumeração para estados dos materiais."""
    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"


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
        if self.nome == MaterialType.WATER.value:
            return {
                MaterialState.SOLID: -0.1,  # Water freezes at 0°C
                MaterialState.LIQUID: 0.1,  # Water melts at 0°C (min liquid)
                MaterialState.GAS: 100.0,  # Water boils at 100°C (gas state)
            }
        elif self.nome == MaterialType.GLASS.value:
            return {
                MaterialState.SOLID: 1000.0,  # Approximate melting point of glass
                MaterialState.LIQUID: 1500.0,  # Approximate melting point
                MaterialState.GAS: float("inf"),  # No boiling in typical conditions
            }
        elif self.nome == MaterialType.ALUMINUM.value:
            return {
                MaterialState.SOLID: 660.0,  # Aluminum melting point
                MaterialState.LIQUID: 661.0,  # Aluminum melting (min liquid)
                MaterialState.GAS: 2500.0,  # Aluminum boiling point
            }
        else:
            return {
                MaterialState.SOLID: float("-inf"),
                MaterialState.LIQUID: float("-inf"),
                MaterialState.GAS: float("inf"),
            }

    def _load_image(self, img_path: str) -> pygame.Surface:
        """Carrega e prepara a imagem do material."""
        try:
            # Try the path as-is first
            if os.path.exists(img_path):
                image = pygame.image.load(img_path).convert_alpha()
                scaled_image = pygame.transform.scale(image, (self.w, self.h))
                return scaled_image

            # If that fails, try relative to project root
            # Get the project root (assuming this file is in src/components)
            project_root = os.path.join(os.path.dirname(__file__), "..", "..")
            full_path = os.path.join(project_root, img_path)
            full_path = os.path.normpath(full_path)

            if os.path.exists(full_path):
                image = pygame.image.load(full_path).convert_alpha()
                scaled_image = pygame.transform.scale(image, (self.w, self.h))
                return scaled_image

            error_msg = f"Arquivo não encontrado: {img_path} ou {full_path}"
            raise FileNotFoundError(error_msg)
        except (pygame.error, FileNotFoundError) as e:
            placeholder = self._create_placeholder_image()
            return placeholder

    def _create_placeholder_image(self) -> pygame.Surface:
        """Cria uma imagem placeholder quando a imagem original não pode ser carregada."""
        image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        # Fill with a visible color for debugging (red-ish) so we can tell it's the placeholder
        image.fill((255, 0, 0, 128))  # Semi-transparent red to make it obvious

        # Draw a border to make it more visible
        pygame.draw.rect(image, (255, 255, 255, 255), (0, 0, self.w, self.h), 3)

        # Draw an X to make it obvious this is a placeholder
        pygame.draw.line(
            image, (255, 255, 255, 255), (5, 5), (self.w - 5, self.h - 5), 3
        )
        pygame.draw.line(
            image, (255, 255, 255, 255), (self.w - 5, 5), (5, self.h - 5), 3
        )

        # Draw some text to indicate this is a placeholder
        try:
            font = pygame.font.SysFont(None, 20)
            text = font.render("NO IMG", True, (255, 255, 255, 255))
            text_rect = text.get_rect(center=(self.w // 2, self.h // 2))
            image.blit(text, text_rect)
        except:
            pass  # If font fails, just continue without text

        return image

    def _update_image_based_on_temperature(self, state: AppState) -> None:
        """Atualiza a imagem do material baseada no estado atual."""
        # Get the active temperature value (in Celsius)
        active_temp_celsius = state.valor_ativo

        # Based on the material type and current temperature, select appropriate image
        target_image_path = None
        if self.nome == MaterialType.WATER.value:
            # Get water state (solid, liquid, gas) based on temperature
            if active_temp_celsius <= self.state_mapping[MaterialState.SOLID]:
                # Solid state - ice
                target_image_path = "src/assets/Agua-solido.png"
            elif active_temp_celsius <= self.state_mapping[MaterialState.GAS]:
                # Liquid state - water
                target_image_path = "src/assets/Agua-liquida.png"
            else:
                # Gas state - steam
                target_image_path = "src/assets/Agua-gasosa.png"

        elif self.nome == MaterialType.GLASS.value:
            # For glass, decide based on temperature
            if active_temp_celsius < self.state_mapping[MaterialState.SOLID]:
                # Solid state - regular glass
                target_image_path = "src/assets/Vidro-solido.png"
            elif active_temp_celsius < self.state_mapping[MaterialState.GAS]:
                # Liquid state (molten glass)
                target_image_path = "src/assets/Vidro-liquida.png"
            else:
                # Gas state (very high temperature)
                target_image_path = "src/assets/Vidro-gasosa.png"

        elif self.nome == MaterialType.ALUMINUM.value:
            # For aluminum, decide based on temperature
            if active_temp_celsius < self.state_mapping[MaterialState.SOLID]:
                # Solid state - solid aluminum
                target_image_path = "src/assets/Aluminio-solido.png"
            elif active_temp_celsius < self.state_mapping[MaterialState.GAS]:
                # Liquid state (molten aluminum)
                target_image_path = "src/assets/Aluminio-liquida.png"
            else:
                # Gas state (very high temperature)
                target_image_path = "src/assets/Aluminio-gasosa.png"

        # Only try to load a new image if we have a target path
        if target_image_path:
            try:
                new_image = self._load_image(target_image_path)
                # Only update if we successfully loaded a new image
                if (
                    new_image is not None
                    and new_image != self._create_placeholder_image()
                ):
                    self.image = new_image
                # If loading fails, keep the current image (don't replace with None or broken image)
            except Exception as e:
                print(f"Erro ao atualizar imagem para {self.nome}: {e}")
                # Keep current image if update fails
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
            surf, self.rect, (0, 0, 0), CORES["material_borda"], 2, 8
        )
