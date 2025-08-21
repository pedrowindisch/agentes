import importlib
import inspect  # <-- keep this

import tkinter as tk
from tkinter import messagebox

# from etapas import PrimeiraEtapa, SegundaEtapaPrototipo
from models import Agente, Estrategia, Grid, Renderizador

etapas_mod = importlib.import_module("etapas")
etapas = [
    cls for name, cls in inspect.getmembers(etapas_mod, inspect.isclass)
    if issubclass(cls, Estrategia) and cls is not Estrategia
]

etapas_descricoes = {cls.nome: (cls, cls.descricao) for cls in etapas}

raiz = tk.Tk()
raiz.title("Agentes [inteligência artificial]")

lista_etapas = tk.Listbox(raiz, width=50, height=10)
for nome in etapas_descricoes.keys():
    lista_etapas.insert(tk.END, nome)

lista_etapas.pack(padx=10, pady=10)

renderizador_atual: Renderizador | None = None 

def selecionar_etapa():
    global renderizador_atual

    if renderizador_atual: renderizador_atual.destruir()

    selecionado = lista_etapas.get(lista_etapas.curselection())
    cls, descricao = etapas_descricoes[selecionado]
    messagebox.showinfo("Descrição", descricao)

    grid = Grid(largura=20, altura=15)
    
    estrategia = cls()
    if hasattr(estrategia, "inicializar_grid"):
        estrategia.inicializar_grid(grid)

    agente = Agente(grid, x=5, y=5, estrategia=estrategia)
    if hasattr(estrategia, "inicializar_agente"):
        estrategia.inicializar_agente(agente)
        
    renderizador = Renderizador(raiz, grid, agente)
    renderizador_atual = renderizador

    def mover():
        agente.mover()
        renderizador.renderizar()
        raiz.after(200, mover)

    mover()

if __name__ == "__main__":
    btn = tk.Button(raiz, text="Executar Etapa", command=selecionar_etapa, width=40)
    btn.pack(pady=(0, 10))

    raiz.mainloop()
