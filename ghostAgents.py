# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
from game import Actions
from game import Agent
from searchAgents import PositionSearchProblem
from util import manhattanDistance


# Implementacao do trabalho, passo 4
# Busca uma rota em que nao ha outros fantasmas, a fim de cercar o pacman.
class GhostAgent(Agent):
    def __init__(self, index):
        self.index = index

    # Implementacao do trabalho
    def getAction(self, state):
        problem = PositionSearchProblem(state)
        problem.startState = state.getGhostPosition(self.index)  # Origem da busca
        problem.goal = state.getPacmanPosition()  #Destino da busca(posicao do Pacman)
        start = problem.getStartState() #Posicao atual do fantasma.


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
                fantasmas = state.getGhostPositions()
                fantasmas.remove(state.getGhostPosition(self.index))
                if not coordAtual[0] in fantasmas: #Se tiver fantasmas no caminho a ser buscado, o no(ramo) nao e inserido na fila.
                    coord, direcao, custo = coordAtual
                    tempPath = list(caminho)
                    if not coord in visitados:
                        visitados.add(coord) #Insere o noAtual no conjunto de visitados
                        tempPath.append(direcao)
                        custoTotal = problem.getCostOfActions(tempPath) + util.manhattanDistance(coord, problem.goal)
                        pilha.push((coord, tempPath), custoTotal)



class RandomGhost(GhostAgent):
    "A ghost that chooses a legal action uniformly at random."

    def getDistribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index): dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    "A ghost that prefers to rush Pacman, or flee when scared."

    def __init__(self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState(self.index)
        legalActions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0] + a[0], pos[1] + a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance(pos, pacmanPosition) for pos in newPositions]
        if isScared:
            bestScore = max(distancesToPacman)
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min(distancesToPacman)
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += (1 - bestProb) / len(legalActions)
        dist.normalize()
        return dist
