from models import Estrategia, Grid

class Agente:
    def explorar_ambiente(self):
        """
        Percorre todas as células do grid e retorna um dicionário com a situação de cada célula:
        - 'livre': célula sem obstáculo
        - 'obstaculo': célula bloqueada
        - 'partida': ponto de partida
        - 'destino': ponto de destino
        """
        situacoes = {}
        for x in range(self.grid.largura):
            for y in range(self.grid.altura):
                celula = self.grid.celulas[x][y]
                if self.grid.ponto_partida_escolhido and (x, y) == (self.grid.ponto_partida_escolhido.x, self.grid.ponto_partida_escolhido.y):
                    situacoes[(x, y)] = 'partida'
                elif self.grid.ponto_destino_escolhido and (x, y) == (self.grid.ponto_destino_escolhido.x, self.grid.ponto_destino_escolhido.y):
                    situacoes[(x, y)] = 'destino'
                elif celula.eh_obstaculo:
                    situacoes[(x, y)] = 'obstaculo'
                else:
                    situacoes[(x, y)] = 'livre'
        return situacoes
    def __init__(self, grid: Grid, x, y, estrategia: Estrategia):
        self.grid = grid
        self.x = x
        self.y = y
        self.estrategia = estrategia

    def mover(self):
        dx, dy = self.estrategia.proximo_passo(self)
        nx, ny = self.x + dx, self.y + dy
        
        if self.grid.eh_livre(nx, ny):
            self.x, self.y = nx, ny

