from models import Agente, Estrategia

import random

class PrimeiraEtapa(Estrategia):
    nome = "Agente reativo simples"
    descricao = "Agente sem memória, decisão de movimento baseada apenas na percepção atual (posição e limites do grid). Grid sem obstáculos."

    def proximo_passo(self, agente: Agente):
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
