import os
import pygame
from typing import Optional
from src.config.settings import CORES, TELA_LARGURA, TELA_ALTURA, STRINGS
from src.core.state import AppState
from src.interface.manager import InterfaceManager
from src.utils.load_images import resource_path


def carregar_wallpaper(
    path: str, largura: int, altura: int
) -> Optional[pygame.Surface]:
    abs_path = resource_path(path)
    if not os.path.exists(abs_path):
        print(f"[main] Wallpaper não encontrado: {abs_path}")
        return None
    try:
        imagem = pygame.image.load(abs_path).convert()
        return pygame.transform.scale(imagem, (largura, altura))
    except Exception as e:
        print(f"[main] Erro ao carregar wallpaper: {e}")
        return None


def main() -> None:
    """
    Função principal do programa, responsável por orquestrar o ciclo de vida da aplicação.
    Segue princípios funcionais: separação de efeitos colaterais, tipagem moderna, modularidade e imutabilidade do estado.
    """
    pygame.init()
    try:
        surface: pygame.Surface = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
        pygame.display.set_caption(STRINGS["titulo_janela"])
        clock: pygame.time.Clock = pygame.time.Clock()
        interface: InterfaceManager = InterfaceManager()
        state: AppState = AppState()
        # Corrigido: use caminho relativo para o asset
        wallpaper: Optional[pygame.Surface] = carregar_wallpaper(
            "assets/wallpaper.jpg", TELA_LARGURA, TELA_ALTURA
        )
    except Exception as e:
        print(f"[main] Falha na inicialização: {e}")
        pygame.quit()
        return

    running: bool = True

    while running:
        # Coleta de eventos (efeito colateral)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Transformação funcional do estado: handle_event é função pura
                novo_state = interface.handle_event(event, state)
                if novo_state is not None and novo_state != state:
                    state = novo_state

        # Renderização (efeito colateral)
        if wallpaper is not None:
            surface.blit(wallpaper, (0, 0))
        else:
            surface.fill(CORES["fundo"])

        interface.render(surface, state)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
