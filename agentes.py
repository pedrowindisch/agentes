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

chk_valor = None  # Checkbox removido

renderizador_atual: Renderizador | None = None 

def iniciar_simulacao(cls, grid) -> Estrategia:
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

    return estrategia

def selecionar_etapa():
    global renderizador_atual

    if renderizador_atual:
        renderizador_atual.destruir()

    selecionado = lista_etapas.get(lista_etapas.curselection())
    cls, descricao = etapas_descricoes[selecionado]
    messagebox.showinfo("Descrição", descricao)

    if cls.__name__ == "QuartaEtapaObservavel":
        grid = Grid(largura=10, altura=11)
    else:
        grid = Grid(largura=20, altura=15)
    
    if chk_valor.get() and cls.permite_adicionar_obstaculos:
        # if path.exists(NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS):
        #     try: grid.obstaculos = pickle.load(file=open(NOME_ARQUIVO_OBSTACULOS_SERIALIZADOS, "rb"))
        #     except Exception as ex: print(ex)
    grid = Grid(largura=20, altura=15)

    # Só a etapa 3.2 permite obstáculos manualmente
    if hasattr(cls, "nome") and cls.nome == "3.2. Agente baseado em objetivos (com obstáculos)
        raiz_montador_cenario = tk.Toplevel(raiz)
        raiz_montador_cenario.title("Montar cenário")

        montador_cenario = MontadorCenario(raiz_montador_cenario, grid)
        montador_cenario.renderizar()

        def concluir():
            raiz_montador_cenario.destroy()
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
    elif hasattr(cls, "nome") and cls.nome == "4.2. Agente Baseado em Utilidade (com obstáculos)":
        raiz_montador_cenario = tk.Toplevel(raiz)
        raiz_montador_cenario.title("Montar cenário")

        montador_cenario = MontadorCenario(raiz_montador_cenario, grid)
        montador_cenario.renderizar()

        def concluir():
            raiz_montador_cenario.destroy()
            estrategia_inst = iniciar_simulacao(cls, grid)
            messagebox.showinfo(
                    "Custo Total",
                    f"O custo total do caminho é: {estrategia_inst.custoTotal}"
                )
                

        txt_instrucoes = tk.Text(
            raiz_montador_cenario,
            height=8,
            width=50,
            wrap="word"
        )
        txt_instrucoes.insert("1.0",
            "clique e arraste (bt. esquerdo) para adicionar/remover obstáculos\n"
            "clique duplo para definir o ponto de PARTIDA (azul).\n"
            "shift + clique duplo para definir o ponto de DESTINO (verde). \n"
            "clique no botão direito para definir o peso das células (1, 2 ou 3)."
        )
        txt_instrucoes.config(state="disabled")
        txt_instrucoes.pack(pady=10)

        btn_concluir = tk.Button(raiz_montador_cenario, text="Concluir", command=concluir)
        btn_concluir.pack(pady=10)

    else:
        iniciar_simulacao(cls, grid)


btn = tk.Button(raiz, text="Executar etapa", command=selecionar_etapa, width=40)
btn.pack(pady=(0, 10))

if __name__ == "__main__":
    raiz.mainloop()
