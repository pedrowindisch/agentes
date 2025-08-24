from functools import partial
import tkinter as tk

from models import Grid

class MontadorCenario:
    TAMANHO_CELULA = 20

    def __init__(self, raiz, grid: Grid):
        self.canvas = tk.Canvas(raiz, width=grid.largura*20, height=grid.altura*20)
        self.canvas.pack()
        self.grid = grid

        self._desenhando = False
        self._desenhando_estado = True # True = obstaculo, Falso = limpando o cenário

        self.canvas.bind("<Button-1>", self.iniciar_mudanca_estado)
        self.canvas.bind("<B1-Motion>", self.mudar_estado_celulas)
        self.canvas.bind("<ButtonRelease-1>", self.parar_mudanca_estado)

        self.canvas.bind("<Double-Button-1>", self.setar_partida)
        self.canvas.bind("<Shift-Double-Button-1>", self.setar_destino)
        
        self.renderizar()
    
    def destruir(self):
        self.canvas.destroy()

    def renderizar(self):
        for x in range(self.grid.largura):
            for y in range(self.grid.altura):
                celula = self.grid.celulas[x][y]
                cor = "#E1E1E1"

                if celula.eh_obstaculo:
                    cor = "#B6B6B6"

                tag = f"celula-{x}-{y}"
                self.canvas.create_rectangle(
                    x*self.TAMANHO_CELULA, y*self.TAMANHO_CELULA, (x+1)*self.TAMANHO_CELULA, (y+1)*self.TAMANHO_CELULA,
                    fill=cor, outline="#B6B6B6", tags=tag
                )

                # self.canvas.tag_bind(
                #     tag, 
                #     "<Button-1", 
                #     partial(self.setar_celula, tag)
                # )

                # self.canvas.tag_bind(
                #     tag, 
                #     "<Double-Button-3>", 
                #     partial(self.setar_partida, tag)
                # )

                # self.canvas.tag_bind(
                #     tag, 
                #     "<Triple-Button-3>", 
                #     partial(self.setar_destino, tag)
                # )

    # def setar_partida(self, tag: str, event):
    #     _, x_str, y_str = tag.split("-")
    #     celula = self.grid.celulas[int(x_str)][int(y_str)]

    #     # remove o obstáculo para setar partida
    #     if celula.eh_obstaculo: celula.eh_obstaculo = False

    #     self.grid.ponto_partida_escolhido = celula

    #     tag = f"celula-{int(x_str)}-{int(y_str)}"
    #     self.canvas.itemconfig(tag, fill="#54828c")

    # def setar_destino(self, tag: str, event):
    #     _, x_str, y_str = tag.split("-")
    #     celula = self.grid.celulas[int(x_str)][int(y_str)]

    #     # remove o obstáculo para setar partida
    #     if celula.eh_obstaculo: celula.eh_obstaculo = False

    #     self.grid.ponto_destino_escolhido = celula

    #     tag = f"celula-{int(x_str)}-{int(y_str)}"
    #     self.canvas.itemconfig(tag, fill="#7e8c54")

    # def setar_celula(self, tag: str, event):
    #     _, x_str, y_str = tag.split("-")
    #     celula = self.grid.celulas[int(x_str)][int(y_str)]

    #     celula.eh_obstaculo = not celula.eh_obstaculo

    #     cor = "#B6B6B6" if celula.eh_obstaculo else "#E1E1E1"
    #     tag = f"celula-{int(x_str)}-{int(y_str)}"
    #     self.canvas.itemconfig(tag, fill=cor)

    def definir_estado_celula(self, x, y, valor: bool):
        celula = self.grid.celulas[x][y]
        if celula.eh_obstaculo == valor:
            return 
        
        celula.eh_obstaculo = valor
        
        cor = "#B6B6B6" if valor else "#E1E1E1"
        
        tag = f"celula-{x}-{y}"
        self.canvas.itemconfig(tag, fill=cor)

    def iniciar_mudanca_estado(self, event):
        x, y = self.retorna_celula_por_coordenadas(event)
        if x is None: return

        celula = self.grid.celulas[x][y]

        self._desenhando_estado = not celula.eh_obstaculo
        self._desenhando = True

        self.definir_estado_celula(x, y, self._desenhando_estado)
    
    def parar_mudanca_estado(self, event):
        self._desenhando = False

    def retorna_celula_por_coordenadas(self, event):
        x = event.x // self.TAMANHO_CELULA
        y = event.y // self.TAMANHO_CELULA

        if 0 <= x < self.grid.largura and 0 <= y < self.grid.altura:
            return int(x), int(y)
        
        return None, None
    
    def mudar_estado_celulas(self, event):
        if not self._desenhando: return

        x, y = self.retorna_celula_por_coordenadas(event)
        if x is None: return

        self.definir_estado_celula(x, y, self._desenhando_estado)

    def setar_partida(self, event):
        x, y = self.retorna_celula_por_coordenadas(event)
        if x is None: return
        
        celula = self.grid.celulas[x][y]
        if celula.eh_obstaculo:
            celula.eh_obstaculo = False
            self.canvas.itemconfig(f"celula-{x}-{y}", fill="#E1E1E1")
        
        self.grid.ponto_partida_escolhido = celula
        self.canvas.itemconfig(f"celula-{x}-{y}", fill="#54828c")

    def setar_destino(self, event):
        x, y = self.retorna_celula_por_coordenadas(event)
        if x is None: return
        
        celula = self.grid.celulas[x][y]
        if celula.eh_obstaculo:
            celula.eh_obstaculo = False
            self.canvas.itemconfig(f"celula-{x}-{y}", fill="#E1E1E1")

        self.grid.ponto_destino_escolhido = celula
        self.canvas.itemconfig(f"celula-{x}-{y}", fill="#7e8c54")