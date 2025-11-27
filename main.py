import pygame
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

if __name__ == "__main__":
    main()
