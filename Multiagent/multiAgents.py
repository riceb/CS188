# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
	"""
	A reflex agent chooses an action at each choice point by examining
	its alternatives via a state evaluation function.

	The code below is provided as a guide.  You are welcome to change
	it in any way you see fit, so long as you don't touch our method
	headers.
	"""


	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
		"""
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()

		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"

		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action)
		newPos = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		food_list = newFood.asList()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"

		food_weight = -1

		if newPos in food_list:
			food_weight = 50
		else:
			for food in food_list:
				dist = manhattanDistance(newPos, food)
				if food_weight == -1:
					food_weight = dist
				else:
					food_weight = min(food_weight, dist)

		num_food = successorGameState.getNumFood()

		ghost_num = -1
		scared_ghost = 0

		for i in range(len(newGhostStates)):
			ghost = newGhostStates[i]
			time = newScaredTimes[i]
			dist = manhattanDistance(newPos, ghost.getPosition())

			if time == 0:
				if ghost_num == -1:
					ghost_num = dist
				else:
					ghost_num = min(food_weight, dist)

		if ghost_num < 2:
			ghost_num = -1000

		# capsule = successorGameState.getCapsules()
		# capsule_weight = 0

		# if newPos in capsule:
		#     capsule_weight = 20
		# else:
		#     for cap in capsule:
		#         dist = manhattanDistance(newPos, cap)
		#         capsule_weight = max(food_weight, 1/dist)

		return successorGameState.getScore() + ghost_num - food_weight - 10 * num_food

def scoreEvaluationFunction(currentGameState):
	"""
	This default evaluation function just returns the score of the state.
	The score is the same one displayed in the Pacman GUI.

	This evaluation function is meant for use with adversarial search agents
	(not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	This class provides some common elements to all of your
	multi-agent searchers.  Any methods defined here will be available
	to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	You *do not* need to make any changes here, but you can if you want to
	add functionality to all your adversarial search agents.  Please do not
	remove anything, however.

	Note: this is an abstract class: one that should not be instantiated.  It's
	only partially specified, and designed to be extended.  Agent (game.py)
	is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action from the current gameState using self.depth
		and self.evaluationFunction.

		Here are some method calls that might be useful when implementing minimax.

		gameState.getLegalActions(agentIndex):
		Returns a list of legal actions for an agent
		agentIndex=0 means Pacman, ghosts are >= 1

		gameState.generateSuccessor(agentIndex, action):
		Returns the successor game state after an agent takes an action

		gameState.getNumAgents():
		Returns the total number of agents in the game

		gameState.isWin():
		Returns whether or not the game state is a winning state

		gameState.isLose():
		Returns whether or not the game state is a losing state
		"""
		"*** YOUR CODE HERE ***"

		def maxi(state, depth, index):
			# check if game is over
			if state.isWin() or state.isLose():
				return self.evaluationFunction(state)

			max_val = -math.inf
			max_act = "Stop"

			for act in state.getLegalActions(index):
				successor = state.generateSuccessor(index, act)
				score = next_function(successor, depth, index + 1)[0]

				if score > max_val:
					max_val = score
					max_act = act

			return (max_val, max_act)

		def mini(state, depth, index):
			min_val = math.inf
			min_act = "Stop"

			# next_function = mini
			# next_index = index + 1
			# next_depth = depth

			# if next_index == state.getNumAgents():
			# 	next_function = maxi
			# 	next_index = 0
			# 	next_depth += 1

			for act in state.getLegalActions(index):
				successor = state.generateSuccessor(index, act)

				if depth + 1 == self.depth and index + 1 == state.getNumAgents():
					score = (self.evaluationFunction(successor), act)[0]
				else:
					score = next_function(successor, depth, index + 1)[0]

				if score < min_val:
					min_val = score
					min_act = act

			return (min_val, min_act)

		def next_function(state, depth, index):
			# end game
			if state.isWin() or state.isLose():
				return (self.evaluationFunction(state), "Stop")
			# restart index and increase depth
			if index == state.getNumAgents():
				return next_function(state, depth + 1, 0)
			# call max (pacman agent)
			if index == 0:
				return maxi(state, depth, index)
			# call min (ghost agent)
			return mini(state, depth, index)

		return maxi(gameState, 0, 0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"

		def maxi(state, depth, index, max_best, min_best):
			# check if game is over
			if state.isWin() or state.isLose():
				return self.evaluationFunction(state)

			max_val = -math.inf
			max_act = "Stop"

			for act in state.getLegalActions(index):
				successor = state.generateSuccessor(index, act)
				score = next_function(successor, depth, index + 1, max_best, min_best)[0]

				if score > max_val:
					max_val = score
					max_act = act

					if max_val > min_best:
						return (max_val, max_act)

					max_best = max(max_val, max_best)

			return (max_val, max_act)

		def mini(state, depth, index, max_best, min_best):
			min_val = math.inf
			min_act = "Stop"

			for act in state.getLegalActions(index):
				successor = state.generateSuccessor(index, act)

				if depth + 1 == self.depth and index + 1 == state.getNumAgents():
					score = (self.evaluationFunction(successor), act)[0]
				else:
					score = next_function(successor, depth, index + 1, max_best, min_best)[0]

				if score < min_val:
					min_val = score
					min_act = act

					if min_val < max_best:
						return (min_val, min_act)

					min_best = min(min_val, min_best)

			return (min_val, min_act)

		def next_function(state, depth, index, max_best, min_best):
			# end game
			if state.isWin() or state.isLose():
				return (self.evaluationFunction(state), "Stop")
			# restart index and increase depth
			if index == state.getNumAgents():
				return next_function(state, depth + 1, 0, max_best, min_best)
			# call max (pacman agent)
			if index == 0:
				return maxi(state, depth, index, max_best, min_best)
			# call min (ghost agent)
			return mini(state, depth, index, max_best, min_best)

		return maxi(gameState, 0, 0, -math.inf, math.inf)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""
	def maxi(self, dpt, gameState):
		if self.depth == dpt or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		results = [gameState.generateSuccessor(0, m) for m in gameState.getLegalActions(0)]
		return max([self.expecti(dpt, 1, state) for state in results])

	def expecti(self, dpt, agentIndex, gameState):
		if self.depth == dpt or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		results = [gameState.generateSuccessor(agentIndex, m) for m in gameState.getLegalActions(agentIndex)]
		if agentIndex == gameState.getNumAgents() - 1:
			scores = [self.maxi(dpt + 1, state) for state in results]
		else:
			scores = [self.expecti(dpt, agentIndex + 1, state) for state in results]
		actionNum = len(scores)
		return sum(scores)/actionNum

	def expectimaxer(self, gameState):
		results = [gameState.generateSuccessor(0, move) for move in gameState.getLegalActions(0)]
		scores = [self.expecti(0, 1, state) for state in results]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices)
		return gameState.getLegalActions(0)[chosenIndex]

	def getAction(self, gameState):
		return self.expectimaxer(gameState)
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	evaluation function (question 5).

	DESCRIPTION: find the closest ghost, scared ghost, food, capsule, along with the numbers of them, weighted.
	"""
	agentNum = currentGameState.getNumAgents()
	foodCount = currentGameState.getNumFood()
	food = currentGameState.getFood().asList()
	capsules= currentGameState.getCapsules()
	ghostsPos = currentGameState.getGhostPositions()
	position = currentGameState.getPacmanPosition()
	newGhostStates = currentGameState.getGhostStates()
	newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

	if foodCount == 0:
		foodDis = 1
	else:
		foodDis = math.inf
		for f in food:
			if util.manhattanDistance(position, f) < foodDis:
				foodDis = util.manhattanDistance(position, f)
		if foodDis == 1:
			foodDis = 100
		if foodDis == 0:
			foodDis = 500


	ghostEval = 0
	ghostSca = 0
	if agentNum > 1:
		ghostDis = math.inf
		for i in range(len(newGhostStates)):
			ghost = newGhostStates[i]
			time = newScaredTimes[i]
			dist = manhattanDistance(position, ghost.getPosition())

			if time == 0:
				ghostDis = min(ghostDis, dist)
				if ghostDis == 2:
					ghostDis = -200
				if ghostDis == 1:
					ghostDis = -1000
				if ghostDis == 3:
					ghostDis = -150
			else:
				if ghostDis == 0:
					ghostsca = 70
				elif ghostDis == 1:
					ghostsca = 40
				else:
					ghostsca = math.inf
					if ghostsca > ghostDis:
						ghostSca = ghostDis
		ghostEval = ghostDis + ghostSca

	capDis = 0
	if len(capsules) > 0:
		capDis = math.inf
		for c in capsules:
			if capDis > util.manhattanDistance(position, c):
				capDis = util.manhattanDistance(position, c)
		if capDis == 0:
			capDis = 40

	return ghostEval + (15 * 1/foodDis - 1) - 3 * foodCount - capDis + currentGameState.getScore()
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
