import math,random
from car import *

import os

class Agent:
  def __init__(self, index=0):
    self.index = index

  def getAction(self, state):
    raiseNotDefined()

"""
class ReflexAgent(Agent):

  def __init__(self):
    self.lastPositions = []
    self.dc = None
    self.chosenAction = []
    self.chosenActionIndex = 1
    self.plannedActions = []

  def getAction(self, gameState):
    if len(self.plannedActions) > 0:
      action = self.plannedActions.pop(0)
      return action

    legalMoves = gameState.getLegalActions()
    gameStateList = []
    for action in legalMoves:
      gameStateList.append((gameState, [action]))
    depth = 25
    while 1:
      gameState, actionHistory = gameStateList.pop(0)

      if len(actionHistory) == depth:
        gameStateList.append((gameState, actionHistory))
        break

      actionPrev = actionHistory[-1]

      newState = gameState.generateSuccessor(actionPrev)
      if newState.isWin():
        self.plannedActions = actionHistory
        action = self.plannedActions.pop(0)
        return action
      
      legalMoves = newState.getLegalActions()
      if len(actionHistory)%10 == 0:
        for action in legalMoves:
          gameStateList.append((newState, actionHistory + [action]))
      elif actionPrev in legalMoves:
        gameStateList.append((newState, actionHistory + [actionPrev]))
      else:
        for action in legalMoves:
          gameStateList.append((newState, actionHistory + [action]))


    scores = []
    for state, action in gameStateList:
      scoreTemp = self.evaluationFunction(state, action[-1])
      scores.append(scoreTemp)
    bestScore = max(scores)

    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best
    action = gameStateList[chosenIndex][1][0]
    self.plannedActions = gameStateList[chosenIndex][1]
    self.plannedActions.pop(0)
    return action

  def evaluationFunction(self, state, action):
    gameState = state.generateSuccessor(action)
    if state.isWin():
      return 99999
    car = gameState.data.agentStates[0].car
    park = gameState.data.layout.getParkingSpace()
    centerCar, orientCar = car.getPosAndOrient()
    centerObs, orientObs = park.getCenterAndOrient()
    dist = ((centerCar[0] - centerObs[0])**2 + (centerCar[1] - centerObs[1])**2)**0.5
    angle = math.atan((centerCar[1] - centerObs[1])/(centerCar[0] - centerObs[0]))
    orientDiff = min([abs(orientCar - orientObs - 3.14159), abs(orientCar - orientObs)])
    numInPark = 0
    for v in car.getVertices():
      if park.contains(v):
        numInPark += 1
    if numInPark == 0: 
      return -dist/250 - abs(angle - orientCar) 
    else:
      return numInPark*100 + 1.0/dist + 0.1/orientDiff# - angle/180*math.pi

  def searchAction(self, gameState):
    bestTotalCost = [float('+inf')]
    bestHistory = [None]
    def recurse(state, totalCost, history):
      if state.isWin():
        if totalCost < bestTotalCost[0]:
          bestTotalCost[0] = totalCost
          bestHistory[0] = history
          return
        if totalCost > 15:
          return
      actionPrev = history[-1]
      for action in state.getLegalActions():
        if action[0] == -actionPrev[0] and action[1] == -actionPrev[1]:
          continue
        newState = state.generateSuccessor(action)
        recurse(newState, totalCost + 1, history + [action])
      return
    recurse(gameState,0,[(0,0)])
    return bestHistory[0]
"""


"""
class Configuration:
  ## A Configuration holds the position of the car 

  def __init__(self, posAndOrient):
    self.posAndOrient = posAndOrient

  def getPosAndOrient(self):
    return self.posAndOrient

  def __hash__(self):
    x = hash(self.posAndOrient[0])
    y = hash(self.posAndOrient[2])
    return hash(x + 13 * y)

  def __str__(self):
    return "(pos, orient) = ("+str(self.posAndOrient[0]) + ", "+str(self.posAndOrient[1]) + ")"

  def generateSuccessor(self, action, L):
    x, y = self.posAndOrient[0]
    theta = self.posAndOrient[1]
    phi = action[0]
    ds = action[1]
    dx = ds * math.cos(theta)
    dy = ds * math.sin(theta)
    dtheta = ds * math.tan(phi) / L
    return Configuration(((x + dx, y + dy), theta + dtheta))
"""
class AgentState:
  """
  AgentState hold the state of a car (configuration)
  """

  def __init__(self, carInit):
    self.car = Car(*carInit)
    
  def getPosAndOrient(self):
    return self.car.getPosAndOrient()

  def duplicate(self):
    copiedAgentState = CopiedAgentState(self.car)
    return copiedAgentState

class CopiedAgentState:
  def __init__(self, car):
    self.car = CopiedCar(car)

  def getPosAndOrient(self):
    return self.car.getPosAndOrient()

  def duplicate(self):
    copiedAgentState = CopiedAgentState(self.car)
    return copiedAgentState

