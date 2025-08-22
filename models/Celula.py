class Celula:
    def __init__(self, x, y, eh_obstaculo=False, peso=1):
        self.x = x
        self.y = y
        self.eh_obstaculo = eh_obstaculo
        self.peso = peso

        self.caractere: str = None
        self.cor: str = None

    def celulas_vizinhas(self) -> list[tuple[int, int]]:
        """Retorna uma lista com as quatro possibilidades de vizinhos. Os vizinhos podem ser INVÁLIDOS (fora do grid), então é preciso validar."""
        return [(self.x, self.y + 1), (self.x + 1, self.y), (self.x, self.y - 1), (self.x - 1, self.y)] 