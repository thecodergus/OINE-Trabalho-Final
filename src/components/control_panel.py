import pygame
from src.config.settings import (
    PAINEL_X, PAINEL_Y, PAINEL_W, PAINEL_H, CORES, FONTES, 
    BOTAO_RAIO, BOTAO_Y, BOTAO_MAIS_X, BOTAO_MENOS_X, FAIXA_LABEL_Y
)
from src.core.state import AppState

class PainelControle:
    def __init__(self, rect: tuple) -> None:
        self.panel_rect = pygame.Rect(rect)
        self.botao_mais = pygame.Rect(
            BOTAO_MAIS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )
        self.botao_menos = pygame.Rect(
            BOTAO_MENOS_X - BOTAO_RAIO,
            BOTAO_Y - BOTAO_RAIO,
            BOTAO_RAIO * 2,
            BOTAO_RAIO * 2,
        )
        self.fator_escala = 2.0  # Fator de multiplicação/divisão

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        if state.arrastando is not None:
            return state
            
        novo_state = state
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_mais.collidepoint(event.pos):
                # Aumentar a proporção (multiplicar ambos os valores)
                novo_min = state.temp_min * self.fator_escala
                novo_max = state.temp_max * self.fator_escala
                
                # Ajustar o valor ativo proporcionalmente
                proporcao = (state.valor_ativo - state.temp_min) / (state.temp_max - state.temp_min)
                novo_valor = novo_min + proporcao * (novo_max - novo_min)
                
                novo_state = AppState(
                    temp_min=novo_min,
                    temp_max=novo_max,
                    escala_ativa=state.escala_ativa,
                    valor_ativo=novo_valor,
                    arrastando=state.arrastando,
                    botao_mais_pressionado=True,
                    botao_menos_pressionado=state.botao_menos_pressionado
                )
            if self.botao_menos.collidepoint(event.pos):
                # Diminuir a proporção (dividir ambos os valores)
                novo_min = state.temp_min / self.fator_escala
                novo_max = state.temp_max / self.fator_escala
                
                # Ajustar o valor ativo proporcionalmente
                proporcao = (state.valor_ativo - state.temp_min) / (state.temp_max - state.temp_min)
                novo_valor = novo_min + proporcao * (novo_max - novo_min)
                
                novo_state = AppState(
                    temp_min=novo_min,
                    temp_max=novo_max,
                    escala_ativa=state.escala_ativa,
                    valor_ativo=novo_valor,
                    arrastando=state.arrastando,
                    botao_mais_pressionado=state.botao_mais_pressionado,
                    botao_menos_pressionado=True
                )
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if state.botao_mais_pressionado or state.botao_menos_pressionado:
                novo_state = AppState(
                    temp_min=state.temp_min,
                    temp_max=state.temp_max,
                    escala_ativa=state.escala_ativa,
                    valor_ativo=state.valor_ativo,
                    arrastando=state.arrastando,
                    botao_mais_pressionado=False,
                    botao_menos_pressionado=False
                )
                
        return novo_state

    def render(self, surf: pygame.Surface, state: AppState) -> None:
        # Removido o desenho do fundo cinza e da borda preta
        # Desenha apenas os botões e o texto
        
        fonte = pygame.font.SysFont(*FONTES["rotulo"])
        txt = fonte.render(
            f"({int(state.temp_min)}, {int(state.temp_max)}) ºC", True, CORES["texto"]
        )
        surf.blit(txt, (PAINEL_X + (PAINEL_W - txt.get_width()) // 2, FAIXA_LABEL_Y))
        
        cor_botao_mais = CORES["botao_clique"] if state.botao_mais_pressionado else CORES["botao_mais"]
        cor_botao_menos = CORES["botao_clique"] if state.botao_menos_pressionado else CORES["botao_menos"]
        
        pygame.draw.circle(
            surf, cor_botao_mais, self.botao_mais.center, BOTAO_RAIO
        )
        pygame.draw.circle(surf, CORES["texto"], self.botao_mais.center, BOTAO_RAIO, 2)
        fonte_b = pygame.font.SysFont(*FONTES["titulo"])
        txt_mais = fonte_b.render("+", True, CORES["texto"])
        surf.blit(
            txt_mais,
            (
                self.botao_mais.centerx - txt_mais.get_width() // 2,
                self.botao_mais.centery - txt_mais.get_height() // 2,
            ),
        )
        
        pygame.draw.circle(
            surf, cor_botao_menos, self.botao_menos.center, BOTAO_RAIO
        )
        pygame.draw.circle(surf, CORES["texto"], self.botao_menos.center, BOTAO_RAIO, 2)
        txt_menos = fonte_b.render("−", True, CORES["texto"])
        surf.blit(
            txt_menos,
            (
                self.botao_menos.centerx - txt_menos.get_width() // 2,
                self.botao_menos.centery - txt_menos.get_height() // 2,
            ),
        )
