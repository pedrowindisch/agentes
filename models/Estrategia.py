from models import Grid


class Estrategia:
    nome: str
    descricao: str

    def inicializar_grid(self, grid: Grid):
        return

    def proximo_passo(self, agente):
        raise NotImplementedError
