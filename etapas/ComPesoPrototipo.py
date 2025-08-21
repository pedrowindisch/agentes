from models import Agente, Estrategia, Grid

import random

class ComPesoPrototipo(Estrategia):
    nome = "Agente reativo com pesos no grid (TESTES/PROTÓTIPO)"
    descricao = "Grid com peso para TESTES."

    def inicializar_grid(self, grid: Grid):
        grid.define_pesos([
            (2, 2, 2), (3, 2, 3), (4, 2, 2),
            (1, 3, 2), (2, 3, 3), (3, 3, 3), (4, 3, 3), (5, 3, 2),
            (2, 4, 2), (3, 4, 3), (4, 4, 2),
        ])

        grid.sinalizar_celula(9, 9, caractere="I")
        grid.sinalizar_celula(5, 5, caractere="F")


    def inicializar_agente(self, agente):
        agente.x = 0
        agente.y = 0

    def proximo_passo(self, agente: Agente):
        # Realiza apenas um movimento aleatório em algumas das direções
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])