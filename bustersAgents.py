# bustersAgents.py
# ----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import util
from game import Agent
from game import Directions
from keyboardAgents import KeyboardAgent
import inference
import busters
import os

class NullGraphics:
    "Placeholder for graphics"
    def initialize(self, state, isBlue = False):
        pass
    def update(self, state):
        pass
    def pause(self):
        pass
    def draw(self, state):
        pass
    def updateDistributions(self, dist):
        pass
    def finish(self):
        pass

class KeyboardInference(inference.InferenceModule):
    """
    Basic inference module for use with the keyboard.
    """
    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if emissionModel[trueDistance] > 0:
                allPossible[p] = 1.0
        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        pass

    def getBeliefDistribution(self):
        return self.beliefs


class BustersAgent:
    "An agent that tracks and displays its beliefs about ghost positions."

    def __init__( self, index = 0, inference = "ExactInference", ghostAgents = None, observeEnable = True, elapseTimeEnable = True):
        inferenceType = util.lookup(inference, globals())
        self.inferenceModules = [inferenceType(a) for a in ghostAgents]
        self.observeEnable = observeEnable
        self.elapseTimeEnable = elapseTimeEnable

        if not os.path.exists("./all_data_pacman.arff"):
            self.attributes = "@attribute pacmanX numeric\n@attribute pacmanY numeric\n@attribute pacmanOR {Stop, East, West, North, South}\n@attribute legalMove1 {Stop, East, West, North, South}\n@attribute legalMove2 {Stop, East, West, North, South}\n@attribute legalMove3 {Stop, East, West, North, South}\n@attribute legalMove4 {Stop, East, West, North, South}\n@attribute legalMove5 {Stop, East, West, North, South}\n@attribute ghost1alive {True, False}\n@attribute ghost2alive {True, False}\n@attribute ghost3alive {True, False}\n@attribute ghost4alive {True, False}\n@attribute ghost1X numeric\n@attribute ghost1Y numeric\n@attribute ghost2X numeric\n@attribute ghost2Y numeric\n@attribute ghost3X numeric\n@attribute ghost3Y numeric\n@attribute ghost4X numeric\n@attribute ghost4Y numeric\n@attribute ghost1distance numeric\n@attribute ghost2distance numeric\n@attribute ghost3distance numeric\n@attribute ghost4distance numeric\n@attribute nearestPacdot numeric\n@attribute score numeric\n@attribute actionTaken {Stop, East, West, North, South}"
            with open("all_data_pacman.arff", "a") as file:
                file.write("@relation 'pacman-info'" + "\n")
                file.write(self.attributes + "\n")
                file.write("@data" + "\n")

    def registerInitialState(self, gameState):
        "Initializes beliefs and inference modules"
        import __main__
        self.display = __main__._display
        for inference in self.inferenceModules:
            inference.initialize(gameState)
        self.ghostBeliefs = [inf.getBeliefDistribution() for inf in self.inferenceModules]
        self.firstMove = True

    def observationFunction(self, gameState):
        "Removes the ghost states from the gameState"
        agents = gameState.data.agentStates
        gameState.data.agentStates = [agents[0]] + [None for i in range(1, len(agents))]
        return gameState

    def getAction(self, gameState):
        "Updates beliefs, then chooses an action based on updated beliefs."
        #for index, inf in enumerate(self.inferenceModules):
        #    if not self.firstMove and self.elapseTimeEnable:
        #        inf.elapseTime(gameState)
        #    self.firstMove = False
        #    if self.observeEnable:
        #        inf.observeState(gameState)
        #    self.ghostBeliefs[index] = inf.getBeliefDistribution()
        #self.display.updateDistributions(self.ghostBeliefs)
        return self.chooseAction(gameState)

    def chooseAction(self, gameState):
        "By default, a BustersAgent just stops.  This should be overridden."
        return Directions.STOP

class BustersKeyboardAgent(BustersAgent, KeyboardAgent):
    "An agent controlled by the keyboard that displays beliefs about ghost positions."

    def __init__(self, index = 0, inference = "KeyboardInference", ghostAgents = None):
        KeyboardAgent.__init__(self, index)
        BustersAgent.__init__(self, index, inference, ghostAgents)

    def getAction(self, gameState):
        return BustersAgent.getAction(self, gameState)

    def chooseAction(self, gameState):
        return KeyboardAgent.getAction(self, gameState)

from distanceCalculator import Distancer
from game import Actions
from game import Directions
import random, sys

'''Random PacMan Agent'''
class RandomPAgent(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        ##print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table
        
    def chooseAction(self, gameState):
        move = Directions.STOP
        legal = gameState.getLegalActions(0) ##Legal position from the pacman
        move_random = random.randint(0, 3)
        if   ( move_random == 0 ) and Directions.WEST in legal:  move = Directions.WEST
        if   ( move_random == 1 ) and Directions.EAST in legal: move = Directions.EAST
        if   ( move_random == 2 ) and Directions.NORTH in legal:   move = Directions.NORTH
        if   ( move_random == 3 ) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move
        
class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that has
        not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (according to mazeDistance!).

        To find the mazeDistance between any two positions, use:
          self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
          successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief
        distributions for each of the ghosts that are still alive.  It
        is defined based on (these are implementation details about
        which you need not be concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.
        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = \
            [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
             if livingGhosts[i+1]]
        return Directions.EAST

class BasicAgentAA(BustersAgent):

    def registerInitialState(self, gameState):
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)
        self.countActions = 0
        
    ''' Example of counting something'''
    def countFood(self, gameState):
        food = 0
        for width in gameState.data.food:
            for height in width:
                if(height == True):
                    food = food + 1
        return food
    
    ''' Print the layout'''  
    def printGrid(self, gameState):
        table = ""
        #print(gameState.data.layout) ## Print by terminal
        for x in range(gameState.data.layout.width):
            for y in range(gameState.data.layout.height):
                food, walls = gameState.data.food, gameState.data.layout.walls
                table = table + gameState.data._foodWallStr(food[x][y], walls[x][y]) + ","
        table = table[:-1]
        return table

    def printInfo(self, gameState):
        print "---------------- TICK ", self.countActions, " --------------------------"
        # Dimensiones del mapa
        width, height = gameState.data.layout.width, gameState.data.layout.height
        print "Width: ", width, " Height: ", height
        # Posicion del Pacman
        print "Pacman position: ", gameState.getPacmanPosition()
        # Acciones legales de pacman en la posicion actual
        print "Legal actions: ", gameState.getLegalPacmanActions()
        # Direccion de pacman
        print "Pacman direction: ", gameState.data.agentStates[0].getDirection()
        # Numero de fantasmas
        print "Number of ghosts: ", gameState.getNumAgents() - 1
        # Fantasmas que estan vivos (el indice 0 del array que se devuelve corresponde a pacman y siempre es false)
        print "Living ghosts: ", gameState.getLivingGhosts()
        # Posicion de los fantasmas
        print "Ghosts positions: ", gameState.getGhostPositions()
        # Direciones de los fantasmas
        print "Ghosts directions: ", [gameState.getGhostDirections().get(i) for i in range(0, gameState.getNumAgents() - 1)]
        # Distancia de manhattan a los fantasmas
        print "Ghosts distances: ", gameState.data.ghostDistances
        # Puntos de comida restantes
        print "Pac dots: ", gameState.getNumFood()
        # Distancia de manhattan a la comida mas cercada
        print "Distance nearest pac dots: ", gameState.getDistanceNearestFood()
        # Paredes del mapa
        print "Map:  \n", gameState.getWalls()
        # Puntuacion
        print "Score: ", gameState.getScore()

    def chooseAction(self, gameState):
        self.countActions += 1
        self.printInfo(gameState)
        self.printLineData(gameState)

        pacmanPos = gameState.getPacmanPosition()
        legalActions = gameState.getLegalPacmanActions()

        # Lista para almacenar las mejores acciones y la distancia minima a los fantasmas
        bestActions = []
        shortestDistance = float("inf")

        # Obtener posiciones de fantasmas y filtrar solo los vivos
        ghostPositions = [pos for index, pos in enumerate(gameState.getGhostPositions()) if gameState.getLivingGhosts()[index + 1]]

        # Iterar sobre cada fantasma vivo para encontrar la distancia mas corta
        for ghostPos in ghostPositions:
            for action in legalActions:
                successorPos = Actions.getSuccessor(pacmanPos, action)
                distance = self.distancer.getDistance(successorPos, ghostPos)
                
                # Actualizar la mejor accion si se encuentra una distancia mas corta
                if distance < shortestDistance:
                    shortestDistance = distance
                    bestActions = [action]  # Comenzar una nueva lista de mejores acciones
                elif distance == shortestDistance:
                    bestActions.append(action)  # Anadir accion empatada a la lista de mejores acciones

        print("Mejores acciones: ", bestActions)
        return random.choice(bestActions) if bestActions else 'Stop'

    def printLineData(self, gameState):
        # Datos relevantes
        pacmanPosition = gameState.getPacmanPosition()
        pacmanDirection = gameState.data.agentStates[0].getDirection()
        livingGhosts = gameState.getLivingGhosts()  # Suma de fantasmas vivos, excluyendo a Pac-Man
        ghostPositions = gameState.getGhostPositions()
        ghostDistances = gameState.data.ghostDistances
        nearestFoodDistance = gameState.getDistanceNearestFood()
        legalmoves = gameState.getLegalPacmanActions()
        score = gameState.getScore()

        # Asegurate de que ghostPositions y ghostDistances tengan siempre 4 elementos
        ghostPositionsPadded = ghostPositions + [(None, None)] * (4 - len(ghostPositions))
        ghostDistancesPadded = ghostDistances + [None] * (4 - len(ghostDistances))
        # Reemplazar 'None' por -1 en la lista 'ghostDistancesPadded'
        
        # Asegurar que livingGhosts tenga siempre 5 elementos, rellenando con False si es necesario
        livingGhostsPadded = livingGhosts + [None] * (5 - len(livingGhosts))

        # Ignorar el primer elemento (Pac-Man) y usar solo los estados de los fantasmas
        livingGhostsFiltered = livingGhostsPadded[1:]  # Esto dara los ultimos 4 elementos

        # Asegurar que legalMoves tenga siempre 5 elementos, rellenando con None si es necesario
        legalMovesPadded = legalmoves + [None] * (5 - len(legalmoves))

        # Preparar la cadena de datos incluyendo los estados de los fantasmas vivos
        dataLine = "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(
            pacmanPosition[0], pacmanPosition[1], pacmanDirection, legalMovesPadded[0], legalMovesPadded[1], legalMovesPadded[2], legalMovesPadded[3], legalMovesPadded[4],
            livingGhostsFiltered[0], livingGhostsFiltered[1], livingGhostsFiltered[2], livingGhostsFiltered[3],
            ghostPositionsPadded[0][0], ghostPositionsPadded[0][1],
            ghostPositionsPadded[1][0], ghostPositionsPadded[1][1],
            ghostPositionsPadded[2][0], ghostPositionsPadded[2][1],
            ghostPositionsPadded[3][0], ghostPositionsPadded[3][1],
            ghostDistancesPadded[0], ghostDistancesPadded[1], ghostDistancesPadded[2], ghostDistancesPadded[3],
            nearestFoodDistance, score
        )

        # Escribir en un archivo (anhadiendo en cada llamada)
        with open("gameData.txt", "a") as file:
            file.write(dataLine + "\n")

        return dataLine