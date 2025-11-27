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

    def handle_event(self, event: pygame.event.Event, state: AppState) -> AppState:
        if state.arrastando is not None:
            return state
            
        novo_state = state
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_mais.collidepoint(event.pos):
                # Aumentar: temp_min = valor_atual - 150, temp_max = valor_atual + 150
                novo_min = state.valor_ativo - 150
                novo_max = state.valor_ativo + 150
                
                # Aplicar limites: temp_min não pode ser menor que -50, temp_max não pode ser menor que 300
                novo_min = max(novo_min, -50.0)
                novo_max = max(novo_max, 300.0)
                
                # Atualizar também o valor ativo (aumenta 10 unidades)
                novo_valor = state.valor_ativo + 10
                # Garantir que o valor esteja dentro dos novos limites
                novo_valor = max(novo_min, min(novo_max, novo_valor))
                
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
                # Correção: quando o botão - é pressionado, deve SUBTRAIR
                # temp_min = valor_atual - 150, temp_max = valor_atual + 150 (mesma lógica do +)
                # Mas o valor ativo deve diminuir
                novo_min = state.valor_ativo - 150
                novo_max = state.valor_ativo + 150
                
                # Aplicar limites: temp_min não pode ser menor que -50, temp_max não pode ser menor que 300
                novo_min = max(novo_min, -50.0)
                novo_max = max(novo_max, 300.0)
                
                # Atualizar também o valor ativo (diminui 10 unidades)
                novo_valor = state.valor_ativo - 10
                # Garantir que o valor esteja dentro dos novos limites
                novo_valor = max(novo_min, min(novo_max, novo_valor))
                
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
