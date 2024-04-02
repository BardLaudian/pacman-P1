# keyboardAgents.py
# -----------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley.
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Directions
from game import GameStateData
from sklearn.preprocessing import OrdinalEncoder
import pandas as pd
import random


##Isa
import sys


class KeyboardAgent(Agent):
   # NOTE: Arrow keys also work.
    WEST_KEY  = 'a'
    EAST_KEY  = 'd'
    NORTH_KEY = 'w'
    SOUTH_KEY = 's'
    STOP_KEY = 'q'

    def __init__( self, index = 0 ):

        self.lastMove = Directions.STOP
        self.index = index
        self.keys = []
        self.previousDf = None  # Inicializar el DataFrame anterior como None

    def printLineData(self, gameState, move):
        # Datos relevantes
        livingGhosts = gameState.getLivingGhosts()
        ghostDistances = gameState.data.ghostDistances
        nearestFoodDistance = gameState.getDistanceNearestFood()
        legalmoves = gameState.getLegalPacmanActions()
        score = gameState.getScore()

        # Asegurar que ghostDistances tenga siempre 4 elementos
        ghostDistancesPadded = ghostDistances + [None] * (4 - len(ghostDistances))
        ghostDistancesPadded = [-1 if distance is None else distance for distance in ghostDistancesPadded]

        # Asegurar que livingGhosts tenga siempre 5 elementos, rellenando con False si es necesario
        livingGhostsPadded = livingGhosts + [False] * (5 - len(livingGhosts))
        livingGhostsFiltered = livingGhostsPadded[1:]  # Ignorando el primer elemento (Pac-Man)

        # Asegurar que legalMoves tenga siempre 5 elementos, rellenando con 'None' si es necesario
        legalMovesPadded = legalmoves + [None] * (5 - len(legalmoves))

        nearestFoodDistance = -1 if nearestFoodDistance is None else nearestFoodDistance

        # Definir los datos
        data = {
            'GhostDist1': [ghostDistancesPadded[0]],
            'GhostDist2': [ghostDistancesPadded[1]],
            'GhostDist3': [ghostDistancesPadded[2]],
            'GhostDist4': [ghostDistancesPadded[3]],
            'LegalMove1': [legalMovesPadded[0]],
            'LegalMove2': [legalMovesPadded[1]],
            'LegalMove3': [legalMovesPadded[2]],
            'LegalMove4': [legalMovesPadded[3]],
            'LegalMove5': [legalMovesPadded[4]],
            'LivingGhost1': [livingGhostsFiltered[0]],
            'LivingGhost2': [livingGhostsFiltered[1]],
            'LivingGhost3': [livingGhostsFiltered[2]],
            'LivingGhost4': [livingGhostsFiltered[3]],
            'NearestFoodDistance': [nearestFoodDistance],
            'Score': [score],
            'Move': [move]
        }

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Si existe un DataFrame anterior, calcular la diferencia de Score y agregarla al nuevo DataFrame
        if self.previousDf is not None:
            lastScore = self.previousDf['Score'].iloc[-1]  # Obtener el ultimo Score del DataFrame anterior
            currentScore = df['Score'].iloc[0]  # Obtener el Score actual
            scoreChange = currentScore - lastScore  # Calcular la diferencia
        else:
            scoreChange = 0  # Si no hay DataFrame anterior, la diferencia es 0

        # Agregar la columna 'ScoreChange' al DataFrame actual
        df['ScoreChange'] = scoreChange

        # Reordenar las columnas explicitamente
        column_order = [
            'LegalMove1', 'LegalMove2', 'LegalMove3', 'LegalMove4', 'LegalMove5',
            'LivingGhost1', 'LivingGhost2', 'LivingGhost3', 'LivingGhost4',
            'GhostDist1', 'GhostDist2', 'GhostDist3', 'GhostDist4',
            'NearestFoodDistance', 'Score', 'Move', 'ScoreChange'
        ]
        
        df = df[column_order]
        self.previousDf = df

        # Anhadir el DataFrame al archivo CSV, sin escribir los nombres de las columnas si el archivo ya existe
        with open("all_data_pacman.arff", "a") as f:
            df.to_csv(f, header=f.tell()==0, index=False)

        return df

    def getAction( self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys = keys_waiting() + keys_pressed()
        if keys != []:
            self.keys = keys

        legal = state.getLegalActions(self.index)
        move = self.getMove(legal)

        if move == Directions.STOP:
            # Try to move in the same direction as before
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal: move = Directions.STOP

        if move not in legal:
            move = random.choice(legal)

        self.lastMove = move
        self.printLineData(state, move)
        return move

    def getMove(self, legal):
        move = Directions.STOP
        if   (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:  move = Directions.WEST
        if   (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal: move = Directions.EAST
        if   (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:   move = Directions.NORTH
        if   (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal: move = Directions.SOUTH
        return move        

        
