from models import Agente, Grid


class Estrategia:
    nome: str
    descricao: str
    custoTotal: 0

    permite_adicionar_obstaculos: bool
    eh_ponderada: bool = False

    def inicializar(self, grid: Grid, agente: Agente):
        return

    def proximo_passo(self, agente):
        raise NotImplementedError
