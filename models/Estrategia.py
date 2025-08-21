from models import Agente, Grid


class Estrategia:
    nome: str
    descricao: str

    def inicializar_grid(self, grid: Grid):
        return
    
    def inicializar_agente(self, agente: Agente):
        return

    def proximo_passo(self, agente):
        raise NotImplementedError
