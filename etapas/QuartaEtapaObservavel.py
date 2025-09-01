# etapas/QuartaEtapaObservavel.py
# -------------------------------------------------------------
# Etapa 4: Agente baseado em utilidade (Dijkstra), grid 10x11
# Terrenos: 1 (verde), 2 (amarelo), 3 (vermelho)
# Origem padrão:  (6,1)  => (5,0)  em 0-based
# Destino padrão: (6,11) => (5,10) em 0-based
# O usuário pode escolher origem/destino na UI (sobrepõe o padrão).
# -------------------------------------------------------------

from models import Agente, Celula, Estrategia, Grid
import heapq
from math import inf

class QuartaEtapaObservavel(Estrategia):
    nome = "4.1. Agente baseado em utilidade (Dijkstra)"
    descricao = "Mapa de custos igual ao quadro (10x11). Dijkstra minimiza o custo total."
    permite_adicionar_obstaculos = True

    # ======= Mapa de custos “pixel-a-pixel” (y=0..10, x=0..9) =======
    # Cada linha abaixo representa uma linha do seu quadro.
    # 1 = verde (normal), 2 = amarelo (arenoso), 3 = vermelho (rochoso)
    # Ajuste livremente se quiser refinar alguma célula.
    COST_MAP = [
        # y=0 (linha do 'i' – o 'i' é apenas overlay visual na UI)
        [1,1,1,1,1,1,1,1,1,1],
        # y=1
        [1,1,1,1,1,1,1,1,1,1],
        # y=2
        [1,1,1,1,1,3,1,1,1,1],
        # y=3
        [1,1,2,2,1,3,3,2,2,1],
        # y=4
        [1,1,2,1,3,3,3,1,2,1],
        # y=5 (linha central do blob vermelho)
        [1,1,2,2,3,3,3,2,2,1],
        # y=6
        [1,1,1,2,3,1,2,2,1,1],
        # y=7
        [1,1,1,2,3,1,1,1,1,1],
        # y=8
        [1,1,1,1,1,1,1,1,1,1],
        # y=9
        [1,1,1,1,1,1,1,1,1,1],
        # y=10 (linha do 'f' – overlay visual)
        [1,1,1,1,1,1,1,1,1,1],
    ]
    # =================================================================

    caminho: list[tuple[int, int]] = []
    partida: tuple[int, int] | None = None
    destino: tuple[int, int] | None = None
    custo_total: int | float = inf

    # -------- aplica o mapa literal ao grid (sem sobrescrever obstáculos) --------
    def _aplicar_cost_map(self, grid: Grid):
        assert grid.largura == 10 and grid.altura == 11, "Grid para a questão 4 deve ser 10x11"
        pesos = []
        for y in range(grid.altura):
            for x in range(grid.largura):
                if (x, y) in grid.obstaculos:
                    continue
                w = self.COST_MAP[y][x]
                pesos.append((x, y, w))
        grid.define_pesos(pesos)

    # ------------------------- inicialização ---------------------------
    def inicializar(self, grid: Grid, agente: Agente):
        # origem/destino padrão (em 0-based)
        default_partida = (5, 0)   # (6,1)  em 1-based
        default_destino = (5, 10)  # (6,11) em 1-based

        # se o usuário escolheu na UI, prevalece
        self.partida = (
            (grid.ponto_partida_escolhido.x, grid.ponto_partida_escolhido.y)
            if grid.ponto_partida_escolhido is not None else default_partida
        )
        self.destino = (
            (grid.ponto_destino_escolhido.x, grid.ponto_destino_escolhido.y)
            if grid.ponto_destino_escolhido is not None else default_destino
        )

        # posiciona o agente
        agente.x, agente.y = self.partida

        # aplica o mapa de custos do quadro
        self._aplicar_cost_map(grid)

        # executa Dijkstra para obter o caminho de menor custo
        self._dijkstra(grid)

        # (visual) pinta o caminho e sinaliza o destino
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
