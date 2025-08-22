from models import Agente, Estrategia

import random

class PrimeiraEtapa(Estrategia):
    nome = "1. Agente reativo simples"
    descricao = "Agente sem memória, decisão de movimento baseada apenas na percepção atual (posição e limites do grid). Grid sem obstáculos."

    permite_adicionar_obstaculos = False

    def proximo_passo(self, agente: Agente):
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
