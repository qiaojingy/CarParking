import math,random
from agent import *
from car import *
import heapq, operator
from collections import Counter
import copy
import game
from actions import Directions
from evaluationFunctions import *
from obstacle import *

class TwoStepAgent(Agent):

	def __init__(self):
		self.lastPositions = []
		self.dc = None
		self.chosenAction = []
		self.chosenActionIndex = 1
		self.plannedActions = []
		self.stateHistory = []

		self.middleState = None
		self.middleStatePos = None
		# self.ActionsFromMiddleState = []
		self.ActionReverse = []
		self.middleStateFound = 0

	def applyActionToState(self, action):

		theta = self.destinationState[1]
		phi = action[0]
		ds = action[1]
		dx = ds * math.cos(theta)
		dy = ds * math.sin(theta)
		dtheta = ds * math.tan(phi) / self.geometry.wheelbase

		center_x = self.destinationState[0][0] + dx
		center_y = self.destinationState[0][1] + dy
		orientation = self.destinationState[1] + dtheta

	def getMiddleState(self, gameState):

		destStateCenterAndOrientInfo = gameState.data.layout.goldenParkingSpace.getCenterAndOrient()

		destinationStateOne = gameState.deepCopy()
		destinationStateOne.data.agentStates[0].car.setPosAndOrient(destStateCenterAndOrientInfo)

		#orient = destStateCenterAndOrientInfo[1]
		#if orient >= 0:
		#destStateCenterAndOrientInfo[1] = orient - 3.14159
		#else:
		#	destStateCenterAndOrientInfo[1] = orient + 3.14159
		destinationStateTwo = gameState.deepCopy()
		destinationStateTwo.data.agentStates[0].car.setPosAndOrientReverse(destStateCenterAndOrientInfo)
		# destinationState.data.agentStates[0].car.setPosAndOrientReverse(destStateCenterAndOrientInfo)

		# print destinationState.getCarPosition()

		numAction = 100
		firstX = 50
		itr = numAction/firstX

		# statein = destinationState
		#destinationStateOne = destinationState
		#destinationStateTwo = destinationState
		'''     
		for t in range(itr):
			print 'beam search'
			ActionsFromMiddleState = self.beamSearch(statein, numAction, gameState)
			print ActionsFromMiddleState
			actionTaken = ActionsFromMiddleState[0:firstX * (1+(t==itr-1))]
			self.ActionReverse += actionTaken
			state = statein
			for i in range(firstX * (1+(t==itr-1))):
				state = state.generateSuccessor_Middle(actionTaken[i])
			statein = state
		'''
		middleStateOne, bestScoreOne = self.beamSearch(destinationStateOne, numAction, gameState)
		middleStateTwo, bestScoreTwo = self.beamSearch(destinationStateTwo, numAction, gameState)

		print bestScoreOne, bestScoreTwo

		print '++++++++++++++++++++++++++++++++'
		self.EvalMiddle(gameState, middleStateOne)
		self.EvalMiddle(gameState, middleStateTwo)


		if bestScoreOne > bestScoreTwo:
			self.middleState = middleStateOne
		else:
			self.middleState = middleStateTwo

		# self.middleState = destinationStateOne
		self.middleStatePos = self.calculateCarPos(self.middleState)

		# self.middleState = statein
		# self.middleStatePos = self.calculateCarPos(self.middleState)
		print self.middleStatePos

		print '---------------============-------------'
		print len(self.ActionReverse)
		print self.ActionReverse
		print Counter(self.ActionReverse)
		

	def beamSearch(self, gameState, numAction, initialState):

		# stateHistory = []

		# carState = gameState.data.agentStates[0].car.getPosAndOrient()
		# (center_x, center_y), Orient = carState
		# Orient = Orient/3.14*180
		# stateHistory.append(((int(center_x), int(center_y)), int(Orient)))

		bestScoreMiddle = float('-inf');
		countMiddle = 0
		bestScoreGameList = []

		beamSearch = 50
		depth = numAction
		gameStateListNextLevel = []
		
		legalMoves = gameState.getLegalActions_Middle()
		# print legalMoves
		
		legalMoves = [x for x in legalMoves if x != (0,0)]
		gameStateList = []
		for action in legalMoves:
			gameStateList.append((gameState, [action]))

		random.shuffle(gameStateList)
		scores = []
		for state, action in gameStateList:
			newState = state.generateSuccessor_Middle(action[-1])
			scoreTemp = self.EvalMiddle(initialState, newState)
			scores.append(scoreTemp)

		if len(gameStateList) > beamSearch:
			
			# print scores
			idx = zip(*heapq.nlargest(beamSearch, enumerate(scores), key=operator.itemgetter(1)))[0]

			gameStateListTemp = []
			for i in idx:
				gameStateListTemp.append(gameStateList[i])

			gameStateList = gameStateListTemp

		bestScoreMiddle = max(scores)
		bestScoreGameList = copy.deepcopy(gameStateList)

		gameStateListBackup = copy.deepcopy(gameStateList)

		while 1:

			if len(gameStateList) > 0:
				gameState, actionHistory = gameStateList.pop(0)
			else:
				if len(gameStateListNextLevel) == 0:
					gameStateList = copy.deepcopy(gameStateListBackup)
				else:
					gameStateList = gameStateListNextLevel
					gameStateListBackup = copy.deepcopy(gameStateList)
					gameStateListNextLevel = []

				if len(gameStateList) > beamSearch:
					random.shuffle(gameStateList)

					scores = []
					for state, action in gameStateList:
						newState = state.generateSuccessor_Middle(action[-1])
						scoreTemp = self.EvalMiddle(initialState, newState)
						scores.append(scoreTemp)

					# print scores
					idx = zip(*heapq.nlargest(beamSearch, enumerate(scores), key=operator.itemgetter(1)))[0]

					gameStateListTemp = []
					for i in idx:
						gameStateListTemp.append(gameStateList[i])

					gameStateList = gameStateListTemp

				scoresSelected = []
				for state, action in gameStateList:
					newState = state.generateSuccessor_Middle(action[-1])
					scoreTemp = self.EvalMiddle(initialState, newState)
					scoresSelected.append(scoreTemp)

				if bestScoreMiddle < max(scoresSelected):
					countMiddle = 0
					bestScoreMiddle = max(scoresSelected)
					bestScoreGameList = copy.deepcopy(gameStateList)
				else:
					countMiddle += 1
					# print countMiddle
					if countMiddle >= 20:
						gameStateList = copy.deepcopy(bestScoreGameList)
						# print len(gameStateList[0][1])
						break

				gameState, actionHistory = gameStateList.pop(0)

			# print len(actionHistory)
			# print gameStateList

			if len(actionHistory) == depth:
				# print len(actionHistory)
				gameStateList.append((gameState, actionHistory))
				break

			actionPrev = actionHistory[-1]
			newState = gameState.generateSuccessor_Middle(actionPrev)
			# print gameState.isLose()
			legalMoves = newState.getLegalActions_Middle()
			# print 'legalMoves', legalMoves
			legalMoves = [x for x in legalMoves if x != (0,0)]
			if len(actionHistory)%10 == 0:
				for action in legalMoves:
					gameStateListNextLevel.append((newState, actionHistory + [action]))
			elif actionPrev in legalMoves:
				gameStateListNextLevel.append((newState, actionHistory + [actionPrev]))
			else:
				for action in legalMoves:
					gameStateListNextLevel.append((newState, actionHistory + [action]))

			# print gameStateListNextLevel

			# print len(gameStateListNextLevel[0][1])

			# print '---------------------'

		# print '123123'
		# print countMiddle
		# print '123123'
		# print len(gameStateList[0][1])
		# print '12123123'

		scores = []
		for state, action in gameStateList:
			newState = state.generateSuccessor_Middle(action[-1])
			scoreTemp = self.EvalMiddle(initialState, newState)
			# print scoreTemp, action
			scores.append(scoreTemp)
		bestScore = max(scores)
		# print 'bestScore', bestScore

		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices)

		action = gameStateList[chosenIndex][1][-1]
		# print action
		carState = gameStateList[chosenIndex][0].generateSuccessor_Middle(action).getCarPosition()
		middleState = gameStateList[chosenIndex][0].generateSuccessor_Middle(action)

		(center_x, center_y), Orient = carState
		Orient = Orient/3.14*180

		# self.middleStatePos = ((int(center_x), int(center_y)), int(Orient))
		
		# (ActionList) = gameStateList[chosenIndex][1]

		# for action in ActionList:
		#	a1, a2 = action
		#	self.ActionsFromMiddleState.append((a1, a2))
		print '================================'
		print len(gameStateList[chosenIndex][1])
		print gameStateList[chosenIndex][1]
		action = gameStateList[chosenIndex][1][-1]
		# return gameStateList[chosenIndex][0].generateSuccessor_Middle(action)

		return (middleState, bestScoreMiddle)

	def isClose(self, pos1, pos2):
		# print "d", (pos1[0][0] - pos2[0][0])**2 + (pos1[0][1] - pos2[0][1])**2
		# print "o", abs(pos1[1] - pos2[1])
		return ((pos1[0][0] - pos2[0][0])**2 + (pos1[0][1] - pos2[0][1])**2 + 10000*abs(pos1[1] - pos2[1]) < 300)

	def EvalMiddle(self, initialState, middleState):

		car = middleState.data.agentStates[0].car
		park = initialState.data.layout.getParkingSpace()
		centerCar, orientCar = car.getPosAndOrient()
		centerObs, orientObs = park.getCenterAndOrient()
		dist = ((centerCar[0] - centerObs[0])**2 + (centerCar[1] - centerObs[1])**2)**0.5
		angle = math.atan((centerCar[1] - centerObs[1])/(centerCar[0] - centerObs[0]))
		# orientDiff = min([abs(orientCar - orientObs - 3.14159), abs(orientCar - orientObs)])
		orientDiff = abs(orientCar - orientObs)

		numInPark = 0
		for v in car.getVertices():
			if park.contains(v):
				numInPark += 1

		print -numInPark*100, dist, 100 * abs(centerCar[1] - centerObs[1]), 0.1/(orientDiff+0.01)
		score1 = -numInPark*100 + dist + 100 * abs(centerCar[1] - centerObs[1])+ 0.1/(orientDiff+0.01)

		carInit = initialState.data.agentStates[0].car
		centerCarInit, orientCarInit = carInit.getPosAndOrient()
		angle = math.atan((centerCar[1] - centerCarInit[1])/(centerCar[0] - centerCarInit[0]))

		if ((centerCar[1] - centerCarInit[1]) > 0 and angle < 0):
			angle += math.pi
		if (centerObs[1] < centerCar[1]) and (angle > 0):
			angle -= math.pi
			# print centerCar, centerCarInit
		bestAngle = 2 * angle - orientCarInit
			# print "angles", angle, orientCarInit, bestAngle, orientCar
		#print "angle", angle
		#print "orientCarInit", orientCarInit
		#print "bestAngle", bestAngle

		score2 = abs(bestAngle - orientCar)
                
		center, orient = car.getCenterAndOrient();
		prot = 50.0
		tail = 20.0
		side = 10.0
		carShade = RecObstacle(center[0] + (prot - tail)/2*math.cos(orient), center[1] + (prot - tail)/2*math.sin(orient), car.geometry.length + prot + tail, car.geometry.width + side, orient)
		num = 0
		layout = initialState.data.layout
		obstacles = layout.getRecObstacles()
		for obstacle in obstacles:
		    for v in carShade.getVertices():
		        if obstacle.contains(v):
		            num += 1
		    for v in obstacle.getVertices():
		        if carShade.contains(v):
		            num += 1
		score3 = -num

		print 0.01*score1, - 40*score2, 60*score3
		return 0.01*score1 - 40*score2 + 60*score3 - 10*abs(centerCarInit[1] - centerCar[1])

	def calculateCarPos(self, gameState):
		carState = gameState.getCarPosition()
		(center_x, center_y), Orient = carState
		Orient = Orient/3.14*180

		return ((int(center_x), int(center_y)), int(Orient))


	def getAction(self, gameState):
		if self.middleState == None:
			print 'compute middle'
			self.getMiddleState(gameState)
			print self.middleStatePos
			input('wait')

		carState = gameState.data.agentStates[0].car.getPosAndOrient()
		(center_x, center_y), Orient = carState
		Orient = Orient/3.14*180
		self.stateHistory.append(((int(center_x), int(center_y)), int(Orient)))

		if len(self.plannedActions) > 0:
			action = self.plannedActions.pop(0)
			return action

		beamSearch = 20
		depth = 50
		firstX = 10
		gameStateListNextLevel = []
		level = 1

		legalMoves = gameState.getLegalActions()
		legalMoves = [x for x in legalMoves if x != (0,0)]
		gameStateList = []
		for action in legalMoves:
			gameStateList.append((gameState, [action]))

		if len(gameStateList) > beamSearch:
			random.shuffle(gameStateList)

			scores = []
			for state, action in gameStateList:
				scoreTemp = self.evaluationFunction(state, action[-1])
				scores.append(scoreTemp)

			idx = zip(*heapq.nlargest(beamSearch, enumerate(scores), key=operator.itemgetter(1)))[0]

			gameStateListTemp = []
			for i in idx:
				gameStateListTemp.append(gameStateList[i])

			gameStateList = gameStateListTemp

		duplicateFlag = 1
		gameStateListBackup = copy.deepcopy(gameStateList)

		while 1:

			if len(gameStateList) > 0:
				gameState, actionHistory = gameStateList.pop(0)
			else:
				if len(gameStateListNextLevel) == 0:
					# threshold /= 2
					duplicateFlag = 0
					gameStateList = copy.deepcopy(gameStateListBackup)
					#print len(gameStateListNextLevel)
					#print '123123123s'
					#print threshold
					#print len(gameStateListBackup)
				else:
					duplicateFlag = 1
					gameStateList = gameStateListNextLevel
					gameStateListBackup = copy.deepcopy(gameStateList)
					#print 'gameStateListBackup'
					#print len(gameStateListBackup)
					gameStateListNextLevel = []

				if len(gameStateList) > beamSearch:
					random.shuffle(gameStateList)

					scores = []
					for state, action in gameStateList:
						scoreTemp = self.evaluationFunction(state, action[-1])
						scores.append(scoreTemp)

					idx = zip(*heapq.nlargest(beamSearch, enumerate(scores), key=operator.itemgetter(1)))[0]

					gameStateListTemp = []
					for i in idx:
						gameStateListTemp.append(gameStateList[i])

					gameStateList = gameStateListTemp

				gameState, actionHistory = gameStateList.pop(0)

			if len(actionHistory) == depth:
				gameStateList.append((gameState, actionHistory))
				break

			actionPrev = actionHistory[-1]

			newState = gameState.generateSuccessor(actionPrev)
			if newState.isWin():
				self.plannedActions = actionHistory
				# self.plannedActions = [x for x in self.plannedActions if x != (0,0)]
				action = self.plannedActions.pop(0)
				#print 'isWin'
				#print action
				return action

			if not self.middleStateFound:
				if self.isClose(self.calculateCarPos(newState), self.middleStatePos):
					input('reach middle state')
					# action = self.ActionsFromMiddleState.pop(-1)
					self.middleStateFound = 1
					self.plannedActions = actionHistory
					action = self.plannedActions.pop(0)
					return action


			carNewState = newState.data.agentStates[0].car.getPosAndOrient()
			(newcenter_x, newcenter_y), newOrient = carNewState
			newOrient = newOrient/3.14*180
			carNewState = ((int(newcenter_x), int(newcenter_y)), int(newOrient))
			#if carNewState in self.stateHistory:
			#  print '___________________'
			#  continue

			if duplicateFlag == 1:
				for carPrevState in self.stateHistory:
					if carNewState == carPrevState:
						newState = None
						break

			#(newcenter_x, newcenter_y), newOrient = carNewState
			#for (precenter_x, precenter_y), prevOrient in self.stateHistory:
			#  x = abs(newcenter_x - precenter_x) < threshold * abs(precenter_x)
			#  y = abs(newcenter_y - precenter_y) < threshold * abs(precenter_y)
			#  theta = abs(newOrient - prevOrient) < threshold * abs(prevOrient)
			#if x == True and y == True and theta == True:
			#  print '---------'
			#  print carNewState, actionPrev
			#  print '========='
			  # newState = None

			if newState == None:
				continue

			legalMoves = newState.getLegalActions()
			legalMoves = [x for x in legalMoves if x != (0,0)]
			if len(actionHistory)%10 == 0:
				for action in legalMoves:
					gameStateListNextLevel.append((newState, actionHistory + [action]))
			elif actionPrev in legalMoves:
				gameStateListNextLevel.append((newState, actionHistory + [actionPrev]))
			else:
				for action in legalMoves:
					gameStateListNextLevel.append((newState, actionHistory + [action]))

		  #print 'next level'
		  #for s in gameStateListNextLevel:
		  #  print s[0].data.agentStates[0].car.getPosAndOrient(), s[1]


		# print len(gameStateList)
		#for s in gameStateList:
		#  print s[0].data.agentStates[0].car.getPosAndOrient(), s[1]

		scores = []
		for state, action in gameStateList:
			scoreTemp = self.evaluationFunction(state, action[-1])
			scores.append(scoreTemp)
		bestScore = max(scores)

		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best
		#print 'best state'
		#print gameStateList[chosenIndex][0].data.agentStates[0].car.getPosAndOrient()
		action = gameStateList[chosenIndex][1][0]
		self.plannedActions = gameStateList[chosenIndex][1]

		# plannedActionsNonStop = [x for x in self.plannedActions if x != (0,0)]

		# print 'plannedActionsNonStop', plannedActionsNonStop

		self.plannedActions = self.plannedActions[0:firstX]
		# if len(self.plannedActions) == 0:
		#  self.plannedActions = [(0,0)]

		# print self.plannedActions 
		# input('')

		self.plannedActions.pop(0)

		#print 'bestMove'
		#print action
		return action

	def evaluationFunction(self, state, action):	

		if self.middleStateFound == 0:
			return EvaluationFunction.evaluateMiddle(state, action, self.middleState)

		else:
			return EvaluationFunction.evaluateParking(state, action)










