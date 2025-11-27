import pygame
import os
from src.config.settings import CORES, TELA_LARGURA, TELA_ALTURA, STRINGS
from src.core.state import AppState
from src.interface.manager import InterfaceManager

def main() -> None:
    pygame.init()
    surface = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption(STRINGS["titulo_janela"])
    clock = pygame.time.Clock()
    interface = InterfaceManager()
    state = AppState()
    running = True

    # Carregar a imagem de wallpaper
    wallpaper_path = "src/assets/wallpaper.jpg"
    if os.path.exists(wallpaper_path):
        wallpaper = pygame.image.load(wallpaper_path).convert()
        # Redimensionar a imagem para cobrir toda a tela
        wallpaper = pygame.transform.scale(wallpaper, (TELA_LARGURA, TELA_ALTURA))
    else:
        wallpaper = None
        print(f"Wallpaper não encontrado: {wallpaper_path}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                state = interface.handle_event(event, state)
        
        # Desenhar o wallpaper ou cor de fundo
        if wallpaper:
            surface.blit(wallpaper, (0, 0))
        else:
            surface.fill(CORES["fundo"])
        
        interface.render(surface, state)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
