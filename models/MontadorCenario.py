from functools import partial
import tkinter as tk

from models import Grid

class MontadorCenario:
    def __init__(self, raiz, grid: Grid):
        self.canvas = tk.Canvas(raiz, width=grid.largura*20, height=grid.altura*20)
        self.canvas.pack()
        self.grid = grid
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
                    x*20, y*20, (x+1)*20, (y+1)*20,
                    fill=cor, outline="#B6B6B6", tags=tag
                )

                self.canvas.tag_bind(
                    tag, 
                    "<Button-1>", 
                    partial(self.setar_celula, tag)
                )

    def setar_celula(self, tag: str, event):
        _, x_str, y_str = tag.split("-")
        celula = self.grid.celulas[int(x_str)][int(y_str)]

        celula.eh_obstaculo = not celula.eh_obstaculo

        cor = "#B6B6B6" if celula.eh_obstaculo else "#E1E1E1"
        tag = f"celula-{int(x_str)}-{int(y_str)}"
        self.canvas.itemconfig(tag, fill=cor)