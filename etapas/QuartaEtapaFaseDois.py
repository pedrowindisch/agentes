from models import Agente, Celula, Estrategia, Grid
import heapq
import random

class QuartaEtapaFaseDois(Estrategia):
    nome = "4.2. Agente baseado em utilidade (com obstáculos)"
    descricao = "Dadas uma posição de partida (x, y) e uma célula de destino (x1, y1), o agente deve encontrar um caminho entre elas considerando o peso das celulas. Grid com obstáculos."
    custoTotal: int = 0

    permite_adicionar_obstaculos = True
    eh_ponderada = True

    caminho: list[tuple[int, int]] = []
    partida: tuple[int, int]
    destino: tuple[int, int]

    def inicializar(self, grid: Grid, agente: Agente):
        # define posições válidas sem obstáculos
        posicoes_validas = [
            (x, y) 
            for x in range(grid.largura)
            for y in range(grid.altura)
            if (x, y) not in grid.obstaculos
        ] 

        self.partida = random.choice(posicoes_validas) if grid.ponto_partida_escolhido is None else (grid.ponto_partida_escolhido.x, grid.ponto_partida_escolhido.y)
        self.destino = random.choice(posicoes_validas) if grid.ponto_destino_escolhido is None else (grid.ponto_destino_escolhido.x, grid.ponto_destino_escolhido.y)

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
        # Dijkstra considerando peso das células
        fila = [(0, (agente.x, agente.y))]  # (custo acumulado, (x, y))

        custo_total = [
            [float("inf") for _ in range(grid.altura)]
            for _ in range(grid.largura)
        ]
        custo_total[agente.x][agente.y] = 0

        grid_espelho = [
            [None for _ in range(grid.altura)]
            for _ in range(grid.largura)
        ]

        while fila:
            custo_atual, (x, y) = heapq.heappop(fila)

            if (x, y) == self.destino:
                break

            celula_atual: Celula = grid.celulas[x][y]

            for vizinho in celula_atual.celulas_vizinhas():
                nx, ny = vizinho
                if not grid.eh_livre(nx, ny) and (nx, ny) != self.destino:
                    continue

                celula_vizinha: Celula = grid.celulas[nx][ny]
                novo_custo = custo_atual + celula_vizinha.peso

                if novo_custo < custo_total[nx][ny]:
                    custo_total[nx][ny] = novo_custo
                    grid_espelho[nx][ny] = (x, y)
                    heapq.heappush(fila, (novo_custo, (nx, ny)))

        # reconstruir caminho
        caminho = []
        celula_atual = self.destino
        while celula_atual is not None:
            caminho.append(celula_atual)
            if celula_atual == (agente.x, agente.y):
                break
            celula_atual = grid_espelho[celula_atual[0]][celula_atual[1]]

        caminho.reverse()
        self.caminho = caminho

        # aqui printa o custo total do caminho
        self.custoTotal = custo_total[self.destino[0]][self.destino[1]]

    def proximo_passo(self, agente: Agente):
        if (agente.x, agente.y) != self.destino:
            indice_atual_caminho = self.caminho.index((agente.x, agente.y))
            proximo_movimento = self.caminho[indice_atual_caminho + 1]

            agente.x = proximo_movimento[0]
            agente.y = proximo_movimento[1]

            return (0, 0)

        return (0, 0)
