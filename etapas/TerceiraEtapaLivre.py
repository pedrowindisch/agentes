from models import Agente, Estrategia

import random

class TerceiraEtapaLivre(Estrategia):
    nome = "Agente baseado em objetivos (ambiente livre)"
    descricao = "Dadas uma posição de partida (x, y) e uma célula de destino (x1, y1), o agente deve encontrar um caminho entre elas. Grid sem obstáculos."

    def proximo_passo(self, agente: Agente):
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
