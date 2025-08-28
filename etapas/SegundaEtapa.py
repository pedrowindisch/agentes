from models import Agente, Estrategia

import random

class SegundaEtapa(Estrategia):
    nome = "2. Agente reativo baseado em modelo"
    descricao = "Agente com memória, decisão de movimento baseado nesta. Seu objetivo é visitar o maior número de células, contornando obstáculos e evitando repetições. Grid sem obstáculos."

    mapa = {}

    permite_adicionar_obstaculos = False

    def proximo_passo(self, agente: Agente):
        direcoes_possiveis = [(1,0), (-1,0), (0,1), (0,-1)]
        proxima_direcao = random.choice(direcoes_possiveis)
        x, y = agente.x + proxima_direcao[0], agente.y + proxima_direcao[1]
        
        # Célula já visitada
        if (x, y) in self.mapa: 
            # Verifica vizinhas
            vizinhas_possiveis = list(map(lambda dir: (agente.x + dir[0], agente.y + dir[1], dir), set(direcoes_possiveis)))
            vizinhas_possiveis.remove((x, y, proxima_direcao))

            livres_nao_visitados = [direcao for direcao in vizinhas_possiveis if agente.grid.eh_livre(direcao[0], direcao[1]) and direcao[2] not in self.mapa]
            # Nesse caso, há células livres, então prioriza essa ao invés da atual. Caso contrário, precisará repetir algum caminho.
            if livres_nao_visitados:
                return random.choice(livres_nao_visitados)[2]
            else:
                livres = [direcao for direcao in vizinhas_possiveis if agente.grid.eh_livre(direcao[0], direcao[1])]

                if livres: 
                    direcao_aleatoria = random.choice(livres)
                    return direcao_aleatoria[2]
            
        if not agente.grid.eh_dentro_do_grid(x, y):
            self.mapa[(x, y)] = False
        elif not agente.grid.eh_livre(x, y):
            self.mapa[(x, y)] = False
        else:
            self.mapa[(x, y)] = True
            return proxima_direcao

        # Não se move e permi
        return (0, 0)