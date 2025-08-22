from models import Agente, Grid


class Estrategia:
    nome: str
    descricao: str

    permite_adicionar_obstaculos: bool

    def inicializar(self, grid: Grid, agente: Agente):
        return

    def proximo_passo(self, agente):
        raise NotImplementedError
