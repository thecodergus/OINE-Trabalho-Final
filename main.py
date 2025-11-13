from typing import Final
import pygame
from model.state import AppState
from view.painel_controle import PainelControle

def main() -> None:
    """Ponto de entrada do simulador educacional de escalas de temperatura."""
    pygame.init()
    WINDOW_SIZE: Final = (1024, 768)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Simulador de Escalas de Temperatura")
    clock = pygame.time.Clock()

    # Estado inicial imutável
    state = AppState(slider_value=20.0)

    # Instancia o painel de controle (View)
    painel = PainelControle(panel_rect=(724, 0, 300, 768))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Atualiza estado via painel (Controller)
            state = painel.handle_event(event, state)

        # Renderização
        screen.fill((240, 240, 240))  # Fundo da janela
        painel.render(screen, state)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
