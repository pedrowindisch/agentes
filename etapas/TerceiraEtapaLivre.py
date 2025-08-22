from collections import deque
from models import Agente, Celula, Estrategia, Grid

import random

class TerceiraEtapaLivre(Estrategia):
    nome = "3.1. Agente baseado em objetivos (ambiente livre)"
    descricao = "Dadas uma posição de partida (x, y) e uma célula de destino (x1, y1), o agente deve encontrar um caminho entre elas. Grid sem obstáculos."

    permite_adicionar_obstaculos = False

    caminho: list[tuple[int, int]] = []
    
    partida: tuple[int, int]
    destino: tuple[int, int]

    def inicializar(self, grid: Grid, agente: Agente):
        # essas são as posições livres, sem obstáculos. criado para que o agente não "nasça" em uma célula proibida.
        posicoes_validas = [
            (x, y) 
            for x in range(grid.largura)
            for y in range(grid.altura)
            if (x, y) not in grid.obstaculos
        ] 

        self.partida = random.choice(posicoes_validas)
        self.destino = random.choice(posicoes_validas)

        agente.x = self.partida[0]
        agente.y = self.partida[1]

        self.calcular_melhor_caminho(grid, agente)
        for (x, y) in self.caminho:
            agente.grid.sinalizar_celula(x, y, cor="#c1e2be")

        agente.grid.sinalizar_celula(
            self.destino[0],
            self.destino[1],
            "D", "#c1e2be"
        )

    def calcular_melhor_caminho(self, grid: Grid, agente: Agente):
        fila = deque([(agente.x, agente.y)])

        # inicializando um grid com todas as células consideradas não visitadas, exceto a célula inicial do agente
        celulas_visitadas = [
            [False for _ in range(grid.altura)]
            for _ in range(grid.largura)
        ]

        grid_espelho = [
            [None for _ in range(grid.altura)]
            for _ in range(grid.largura)
        ]

        celulas_visitadas[agente.x][agente.y] = True

        while len(fila) != 0:
            x, y = fila.popleft()
            if (x, y) == self.destino: break

            celula_atual: Celula = grid.celulas[x][y]

            for vizinho in celula_atual.celulas_vizinhas():
                if not grid.eh_livre(vizinho[0], vizinho[1]): continue
                if celulas_visitadas[vizinho[0]][vizinho[1]]: continue

                celulas_visitadas[vizinho[0]][vizinho[1]] = True
                grid_espelho[vizinho[0]][vizinho[1]] = (x, y)

                fila.append(vizinho)

        
        caminho = []
        celula_atual = self.destino

        while celula_atual is not None:
            caminho.append(celula_atual)
            if celula_atual == self.partida:
                break

            celula_atual = grid_espelho[celula_atual[0]][celula_atual[1]]

        caminho.reverse()
        self.caminho = caminho

    def proximo_passo(self, agente: Agente):
        if (agente.x, agente.y) != self.destino:
            indice_atual_caminho = self.caminho.index(((agente.x, agente.y)))

            proximo_movimento = self.caminho[indice_atual_caminho + 1]
            
            agente.x = proximo_movimento[0]
            agente.y = proximo_movimento[1]

            return (0, 0)

        return (0,0)
