# pacmanAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random

import game
import util
from game import Agent
from pacman import Directions
from searchAgents import PositionSearchProblem


# Implementacao do trabalho, passo 5
# Busca uma rota para a comida mais proxima que nao tenha fantasmas(algoritmo de manhattan), utilizando o algoritmo A*.
class PacmanAgent(game.Agent):
    def getAction(self, state):
        problem = PositionSearchProblem(state)
        problem.startState = state.getPacmanPosition()
        start = problem.getStartState()

        comidaGrid = state.getFood()
        listaDeComidas = list(comidaGrid.asList())  # Lista com as coordenadas de todas as comidas.

        distancia, comida = min([(util.manhattanDistance(start, comida), comida) for comida in listaDeComidas])  # Obtem a comida mais proxima do Pacman utilizando a distancia de manhattan.
        problem.goal = comida

        pilha = util.PriorityQueue()
        pilha.push((start, []), 0)
        visitados = set([start]) #Conjunto dos percorridos
        while not pilha.isEmpty():
            noAtualTupla = pilha.pop()
            noAtual = noAtualTupla[0]
            caminho = noAtualTupla[1]

            if problem.isGoalState(noAtual):
                return caminho[0] #Retorna apenas a primeira acao da lista de acoes retornada pelo algoritmo A*.

            for coordAtual in problem.getSuccessors(noAtual):
                if not coordAtual[0] in state.getGhostPositions(): #Se tiver fantasmas no caminho a ser buscado, o ramo nao e inserido na fila.
                    coord, direcao, custo = coordAtual
                    tempPath = list(caminho)
                    if not coord in visitados:
                        visitados.add(coord) #Insere o noAtual no conjunto de visitados
                        tempPath.append(direcao)
                        custoTotal = problem.getCostOfActions(tempPath) + util.manhattanDistance(coord, problem.goal)
                        pilha.push((coord, tempPath), custoTotal)


class LeftTurnAgent(game.Agent):
    "An agent that turns left at every opportunity"

    def getAction(self, state):
        legal = state.getLegalPacmanActions()
        current = state.getPacmanState().configuration.direction
        if current == Directions.STOP: current = Directions.NORTH
        left = Directions.LEFT[current]
        if left in legal: return left
        if current in legal: return current
        if Directions.RIGHT[current] in legal: return Directions.RIGHT[current]
        if Directions.LEFT[left] in legal: return Directions.LEFT[left]
        return Directions.STOP


class GreedyAgent(Agent):
    def __init__(self, evalFn="scoreEvaluation"):
        self.evaluationFunction = util.lookup(evalFn, globals())
        assert self.evaluationFunction != None

    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        if Directions.STOP in legal: legal.remove(Directions.STOP)

        coordAtualessors = [(state.generatecoordAtualessor(0, action), action) for action in legal]
        scored = [(self.evaluationFunction(state), action) for state, action in coordAtualessors]
        bestScore = max(scored)[0]
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        return random.choice(bestActions)


def scoreEvaluation(state):
    return state.getScore()
