# agentes 🤖

Simulações de agentes - projeto para a disciplina de Inteligência Artificial

## Tópicos/sumário
- [Etapas](#etapas)
- [Adicionando simulações](#adicionando-simulações)
- [Rodando o projeto](#rodando-o-projeto)

## Etapas
- [X] Primeira etapa (agente reativo simples): agente sem memória, decisão de movimento baseada apenas na percepção atual (posição e limites do grid). Grid sem obstáculos.
- [ ] Segunda etapa (agente reativo baseado em modelos): agente com memória, objetivo de visitar o maior número possível de células do grid, evitando repetir já visitadas. Grid com obstáculos.
- [X] Terceira etapa (agente baseado em objetivos): dividida em duas fases.
    - [X] Ambiente livre: grid vazio, com início e fim desconhecidos a priori
    - [X] Ambiente com obstáculos: agente capaz de encontrar o caminho desviando de obstáculos.
- [ ] Quarta etapa (agente baseado em utilidade): dividida em duas fases:
    - [ ] Ambiente completamente observável
    - [ ] Ambiente parcialmente observável

Os itens sinalizados já estão finalizados.

## Adicionando simulações

Para novas simulações, é necessário criar a mesma no diretório `/etapas`, implementando a classe [`Estrategia`](/models/Estrategia.py), como abaixo:

```python
class PrimeiraEtapa(Estrategia):
    nome = "Agente reativo simples"
    descricao = "Agente sem memória, decisão de movimento baseada apenas na percepção atual (posição e limites do grid). Grid sem obstáculos."

    def proximo_passo(self, agente: Agente):
        # Realiza apenas um movimento aleatório em algumas das direções
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
```

Todas as informações para o desenvolvimento de algoritmos podem ser encontrados no parâmetro `agente` (o grid, as células, posição atual do agente, etc.).

Caso seja necessário modificar o grid antes da execução da simulação (gerar obstáculos, gerar pesos para as células), sobrescreva o método `inicializar` da classe:

```python
class SegundaEtapaPrototipo(Estrategia):
    nome = "Agente reativo baseado em modelo (protótipo)"
    descricao = "Agente sem memória, mas que evita obstáculos no grid."

    def inicializar(self, grid: Grid, agente: Agente):
        # grid.define_pesos([
        #     (2, 2, 2), (3, 2, 3), (4, 2, 2),
        #     (1, 3, 2), (2, 3, 3), (3, 3, 3), (4, 3, 3), (5, 3, 2),
        #     (2, 4, 2), (3, 4, 3), (4, 4, 2),
        # ])
        grid.define_obstaculos([(2, 3), [2, 4], [2, 5], [3, 5], [8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [7, 9], [6, 9]])


    def proximo_passo(self, agente: Agente):
        # Realiza apenas um movimento aleatório em algumas das direções
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
```

Da mesma forma, é possível modificar o estado do agente antes de executar a simulação (para, por exemplo, definir a posição inicial dele), como abaixo:

```python
class SegundaEtapaPrototipo(Estrategia):
    nome = "Agente reativo baseado em modelo (protótipo)"
    descricao = "Agente sem memória, mas que evita obstáculos no grid."

    # ... 

    def inicializar(self, grid, agente):
        agente.x = 0
        agente.y = 0

    # ...
```

É possível também sinalizar células com algum caractere/código, como, por exemplo, para destacar a célula inicial/final da etapa:

```python
class ComPesoPrototipo(Estrategia):
    nome = "Agente reativo com pesos no grid (TESTES/PROTÓTIPO)"
    descricao = "Grid com peso para TESTES."

    def inicializar(self, grid: Grid, agente: Agente):
        grid.define_pesos([
            (2, 2, 2), (3, 2, 3), (4, 2, 2),
            (1, 3, 2), (2, 3, 3), (3, 3, 3), (4, 3, 3), (5, 3, 2),
            (2, 4, 2), (3, 4, 3), (4, 4, 2),
        ])

        grid.sinalizar_celula(9, 9, caractere="I")
        grid.sinalizar_celula(5, 5, caractere="F")

    # ...
```

Após isso, adicione a classe no [`__init__.py`](/etapas/__init__.py).

## Rodando o projeto

Com o Python instalado na máquina (versão mínima >= 3.9), crie um ambiente virtual no diretório do projeto:

```bash
# Linux
$ python -m venv venv
    ...
$ source venv/bin/activate 
```

Ou no Windows:

```powershell
> python -m venv venv
    ...
> \venv\Scripts\activate
```

Após isso, rodar o comando `python agentes.py`.

O projeto não tem dependências/bibliotecas para instalação.