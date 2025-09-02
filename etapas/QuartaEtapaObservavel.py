from models import Agente, Celula, Estrategia, Grid
import heapq
from math import inf

class QuartaEtapaObservavel(Estrategia):
    nome = "4.1. Agente baseado em utilidade (Dijkstra)"
    descricao = "Mapa de custos igual ao quadro (10x11). Dijkstra minimiza o custo total."

    permite_adicionar_obstaculos = True
    eh_ponderada = True

    COST_MAP = []
    caminho: list[tuple[int, int]] = []
    partida: tuple[int, int] | None = None
    destino: tuple[int, int] | None = None
    custo_total: int | float = inf


    # -------- aplica o mapa literal ao grid (sem sobrescrever obstáculos) --------
    def _aplicar_cost_map(self, grid: Grid):
        pesos = []
        for y in range(grid.altura):
            for x in range(grid.largura):
                if (x, y) in grid.obstaculos:
                    continue
                w = self.COST_MAP[y][x]
                pesos.append((x, y, w))

        grid.define_pesos(pesos)

    def inicializar(self, grid: Grid, agente: Agente):
        self.COST_MAP = [[1 for x in range(grid.largura)] for y in range(grid.altura)]

        default_partida = (5, 0)   # (6,1)  em 1-based
        default_destino = (5, 10)  # (6,11) em 1-based

        self.partida = (grid.ponto_partida_escolhido.x, grid.ponto_partida_escolhido.y) if grid.ponto_partida_escolhido is not None else default_partida
        self.destino = (grid.ponto_destino_escolhido.x, grid.ponto_destino_escolhido.y) if grid.ponto_destino_escolhido is not None else default_destino

        agente.x, agente.y = self.partida

        self._aplicar_cost_map(grid)

        self._dijkstra(grid)

        for (x, y) in self.caminho:
            agente.grid.sinalizar_celula(x, y, cor="#c1e2be")

        agente.grid.sinalizar_celula(self.destino[0], self.destino[1], "D", "#c1e2be")

    # ----------------------------- Dijkstra ---------------------------
    def _dijkstra(self, grid: Grid):
        sx, sy = self.partida
        tx, ty = self.destino

        dist = [[inf for _ in range(grid.altura)] for _ in range(grid.largura)]
        prev = [[None for _ in range(grid.altura)] for _ in range(grid.largura)]

        dist[sx][sy] = 0
        pq = [(0, (sx, sy))]

        while pq:
            d, (x, y) = heapq.heappop(pq)
            if (x, y) == (tx, ty):
                break
            if d > dist[x][y]:
                continue
            for nx, ny in self._vizinhos(grid, x, y):
                if not grid.eh_livre(nx, ny):
                    continue
                nd = d + self._peso(grid, nx, ny)  # custo para entrar no vizinho
                if nd < dist[nx][ny]:
                    dist[nx][ny] = nd
                    prev[nx][ny] = (x, y)
                    heapq.heappush(pq, (nd, (nx,ny)))

        self._reconstruir_caminho(prev, dist, (sx, sy), (tx, ty))

    # helpers
    def _peso(self, grid: Grid, x: int, y: int) -> int:
        return getattr(grid.celulas[x][y], "peso", 1)

    def _vizinhos(self, grid: Grid, x: int, y: int):
        cel: Celula = grid.celulas[x][y]
        return cel.celulas_vizinhas()

    def _reconstruir_caminho(self, prev, dist, start, goal):
        sx, sy = start
        tx, ty = goal
        if prev[tx][ty] is None and start != goal:
            self.caminho, self.custo_total = [start], inf
            return
        caminho, cur = [], (tx, ty)
        while cur is not None:
            caminho.append(cur)
            if cur == start:
                break
            cx, cy = cur
            cur = prev[cx][cy]
        caminho.reverse()
        self.caminho = caminho
        self.custo_total = dist[tx][ty]

    # animação
    def proximo_passo(self, agente: Agente):
        if (agente.x, agente.y) != self.destino and self.caminho:
            i = self.caminho.index((agente.x, agente.y))
            agente.x, agente.y = self.caminho[i + 1]
        return (0, 0)
