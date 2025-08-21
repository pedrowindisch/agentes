class Celula:
    def __init__(self, x, y, eh_obstaculo=False, peso=1):
        self.x = x
        self.y = y
        self.eh_obstaculo = eh_obstaculo
        self.peso = peso