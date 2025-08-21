# agentes 🤖

Simulações de agentes - projeto para a disciplina de Inteligência Artificial

## Adicionando simulações

Para novas simulações, é necessário criar uma classe no diretório `/etapas` que implemente a classe [`Estrategia`](/models/Estrategia.py), como abaixo:

```python
class PrimeiraEtapa(Estrategia):
    nome = "Agente reativo simples"
    descricao = "Agente sem memória, decisão de movimento baseada apenas na percepção atual (posição e limites do grid). Grid sem obstáculos."

    def proximo_passo(self, agente: Agente):
        # Realiza apenas um movimento aleatório em algumas das direções
        return random.choice([(1,0), (-1,0), (0,1), (0,-1)])
```

Todas as informações para o desenvolvimento de algoritmos podem ser encontrados no parâmetro `agente` (o grid, as células, posição atual do agente, etc.).

Caso seja necessário modificar o grid antes da execução da simulação (gerar obstáculos, gerar pesos para as células), sobrescreva o método `inicializar_grid` da classe:

```python
class SegundaEtapaPrototipo(Estrategia):
    nome = "Agente reativo baseado em modelo (protótipo)"
    descricao = "Agente sem memória, mas que evita obstáculos no grid."

    def inicializar_grid(self, grid: Grid):
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