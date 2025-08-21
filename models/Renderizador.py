import tkinter as tk

from models import Grid

class Renderizador:
    def __init__(self, raiz, grid: Grid, agente):
        self.canvas = tk.Canvas(raiz, width=grid.largura*20, height=grid.altura*20)
        self.canvas.pack()
        self.grid = grid
        self.agente = agente
        self.renderizar()
    
    def destruir(self):
        self.canvas.destroy()

    def renderizar(self):
        exibir_pesos = self.grid.eh_ponderado()

        self.canvas.delete("all")
        for x in range(self.grid.largura):
            for y in range(self.grid.altura):
                celula = self.grid.celulas[x][y]
                cor = "#E1E1E1"

                if celula.eh_obstaculo:
                    cor = "#B6B6B6"

                if exibir_pesos:
                    # todo: ajustar pra ser algo mais dinâmico... meio que uma escala de cores, já que o peso pode ser "dinâmico" (ir de 1 a 5... 1 a 10, etc. etc.), e não
                    # fixamente de 1 a 3
                    if celula.peso == 1:
                        cor = "#CFFDBC"
                    elif celula.peso == 2:
                        cor = "#FFCD98"
                    else:
                        cor = "#E78587"

                    # nesse caso, a célula está sinalizada (pode ser célula de início, célula fim, etc.)
                    if celula.caractere is not None: cor = "#E1E1E1"

                self.canvas.create_rectangle(
                    x*20, y*20, (x+1)*20, (y+1)*20,
                    fill=cor, outline="#B6B6B6" if not exibir_pesos else ""
                )

                if exibir_pesos and celula.caractere is None:
                    self.canvas.create_text(
                        x * 20 + 10, y * 20 + 10, 
                        text=str(celula.peso),
                        fill="#000",
                        font=("Arial", 6, "normal")
                    )

                if celula.caractere is not None:
                    self.canvas.create_text(
                        x * 20 + 10, y * 20 + 10, 
                        text=str(celula.caractere),
                        fill="#000",
                        font=("Arial", 6, "normal")
                    )

        self.canvas.create_oval(
            self.agente.x * 20+4, self.agente.y * 20+4,
            (self.agente.x+1) * 20-4, (self.agente.y+1) * 20-4,
            fill="#555555", outline=""
        )
