from models import Agente, Estrategia, Grid

import random

class SegundaEtapaPrototipo(Estrategia):
    nome = "Agente reativo baseado em modelo (TESTES/PROTÓTIPO)"
    descricao = "Agente sem memória, mas que evita obstáculos no grid."

    def inicializar_grid(self, grid: Grid):
        # grid.define_pesos([
        #     (2, 2, 2), (3, 2, 3), (4, 2, 2),
        #     (1, 3, 2), (2, 3, 3), (3, 3, 3), (4, 3, 3), (5, 3, 2),
        #     (2, 4, 2), (3, 4, 3), (4, 4, 2),
        # ])
        grid.define_obstaculos([(2, 3), [2, 4], [2, 5], [3, 5], [8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [7, 9], [6, 9]])

    def inicializar_agente(self, agente):
        agente.x = 0
        agente.y = 0

    def proximo_passo(self, agente: Agente):
        # Realiza apenas um movimento aleatório em algumas das direções
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])