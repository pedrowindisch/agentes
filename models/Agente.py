from models import Estrategia, Grid

class Agente:
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

