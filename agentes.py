import importlib
import inspect  # <-- keep this

from os import path, remove
import pickle

import tkinter as tk
from tkinter import messagebox

# from etapas import PrimeiraEtapa, SegundaEtapaPrototipo
from models import Agente, Estrategia, Grid, MontadorCenario, Renderizador

NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS = "obstaculos"

etapas_mod = importlib.import_module("etapas")
etapas = [
    cls for name, cls in inspect.getmembers(etapas_mod, inspect.isclass)
    if issubclass(cls, Estrategia) and cls is not Estrategia
]

etapas_descricoes = {cls.nome: (cls, cls.descricao) for cls in etapas}

raiz = tk.Tk()
raiz.title("Agentes [inteligência artificial]")

lista_etapas = tk.Listbox(raiz, width=50, height=10)
for nome in sorted(etapas_descricoes.keys()):
    lista_etapas.insert(tk.END, nome)

lista_etapas.pack(padx=10, pady=10)

chk_valor = tk.BooleanVar()
chk = tk.Checkbutton(raiz, text="Deseja inserir os obstáculos manualmente?", variable=chk_valor)
chk.pack(pady=(0, 10))

renderizador_atual: Renderizador | None = None 

def iniciar_simulacao(cls, grid):
    """Inicia a simulação no grid já montado (com ou sem obstáculos)."""
    global renderizador_atual

    estrategia = cls()
    agente = Agente(grid, x=0, y=0, estrategia=estrategia)

    if hasattr(estrategia, "inicializar"):
        estrategia.inicializar(grid, agente)

    renderizador = Renderizador(raiz, grid, agente)
    renderizador_atual = renderizador

    def mover():
        agente.mover()
        renderizador.renderizar()
        raiz.after(300, mover)

    mover()

def selecionar_etapa():
    global renderizador_atual

    if renderizador_atual: renderizador_atual.destruir()

    selecionado = lista_etapas.get(lista_etapas.curselection())
    cls, descricao = etapas_descricoes[selecionado]
    messagebox.showinfo("Descrição", descricao)

    grid = Grid(largura=20, altura=15)

    if chk_valor.get() and cls.permite_adicionar_obstaculos:
        # if path.exists(NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS):
        #     try: grid.obstaculos = pickle.load(file=open(NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS, "rb"))
        #     except Exception as ex: print(ex)

        raiz_montador_cenario = tk.Toplevel(raiz)
        raiz_montador_cenario.title("Montar cenário")

        montador_cenario = MontadorCenario(raiz_montador_cenario, grid)
        montador_cenario.renderizar()

        def concluir():
            raiz_montador_cenario.destroy()

            # salvando os obstáculos para não precisar "recolocar" eles depois
            # with open(NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS, "wb") as arq:
            #     pickle.dump(grid.obstaculos, arq)

            iniciar_simulacao(cls, grid)

        txt_instrucoes = tk.Text(
            raiz_montador_cenario,
            height=6,       
            width=50,       
            wrap="word"     
        )
        txt_instrucoes.insert("1.0", 
            "clique e arraste (bt. esquerdo) para adicionar/remover obstáculos\n"
            "clique duplo para definir o ponto de PARTIDA (azul).\n"
            "shift + clique duplo para definir o ponto de DESTINO (verde)."
        )
        txt_instrucoes.config(state="disabled") 
        txt_instrucoes.pack(pady=10)

        btn_concluir = tk.Button(raiz_montador_cenario, text="Concluir", command=concluir)
        btn_concluir.pack(pady=10)
    else:
        if chk_valor.get() and not cls.permite_adicionar_obstaculos:
            messagebox.showwarning("Cenário", "Não é possível adicionar obstáculos para esse cenário/etapa")

        iniciar_simulacao(cls, grid)


btn = tk.Button(raiz, text="Executar etapa", command=selecionar_etapa, width=40)
btn.pack(pady=(0, 10))

if __name__ == "__main__":
    raiz.mainloop()
