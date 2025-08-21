from models import Celula

class Grid:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.celulas: list[list[Celula]] = [
            [Celula(x, y) for y in range(altura)] 
            for x in range(largura)
        ]

    def define_obstaculo(self, x, y):
        if self.eh_dentro_do_grid(x, y):
            self.celulas[x][y].eh_obstaculo = True

    def define_obstaculos(self, pontos: list[tuple[int, int]]):
        for (x, y) in pontos:
            self.define_obstaculo(x, y)

    def define_peso(self, x: int, y: int, peso: int):
        if self.eh_dentro_do_grid(x, y):
            self.celulas[x][y].peso = peso

    def define_pesos(self, pontos: list[tuple[int, int, int]]):
        for (x, y, peso) in pontos:
            self.define_peso(x, y, peso)

    def sinalizar_celula(self, x: int, y: int, caractere = None, cor = None):
        self.celulas[x][y].caractere = caractere
        self.celulas[x][y].cor = cor

    def eh_ponderado(self):
        ponderado = False

        for linha in self.celulas:
            for celula in linha:
                if celula.peso != 1: ponderado = True
        
        return ponderado

    def eh_dentro_do_grid(self, x, y):
        return 0 <= x < self.largura and 0 <= y < self.altura

    def eh_livre(self, x, y):
        return self.eh_dentro_do_grid(x, y) and not self.celulas[x][y].eh_obstaculo