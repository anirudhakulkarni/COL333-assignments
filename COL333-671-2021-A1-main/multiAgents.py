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
import random
import util

from game import Agent

# parameters for betterEvaluationFunction
q_param = 100
r_param = 1e10
s_param = 1e10


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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        # print(scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)
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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # strategy 1:
        # if the ghost is scared, then we want to go to the ghost
        # if the ghost is not scared, then we want to go to the closest food
        # if the ghost is not scared, then we want to go to the closest ghost

        ghost_score = 0
        # score due to food
        if successorGameState.isWin():
            return 1e11
        if successorGameState.isLose():
            ghost_score-=1e11
        maxscore = 0
        minsofar = 1e10
        maxsofar = -1e10
        if len(newFood.asList()) == 0:
            minsofar = 0
            maxsofar = 0
        for food in newFood.asList():
            minsofar = min(minsofar, manhattanDistance(newPos, food))
        for food1 in newFood.asList():
            for food2 in newFood.asList():
                maxsofar = max(maxsofar, manhattanDistance(food1, food2))
        food_score = -minsofar-10*len(newFood.asList())-maxsofar
        # score due to ghost
        
        if len(newGhostStates)==0:
            return 
        for ghost in newGhostStates:
            if ghost.scaredTimer > 0:
                # scared ghost
                if manhattanDistance(newPos, ghost.getPosition()) < 2:
                    return ghost_score+1e9
                else:
                    ghost_score += q_param / \
                        manhattanDistance(newPos, ghost.getPosition())

            else:
                if manhattanDistance(newPos, ghost.getPosition()) < 2:
                    ghost_score -= 1e10
                else:
                    ghost_score -= q_param / \
                        manhattanDistance(newPos, ghost.getPosition())
        # print(food_distance, ghost_score)
        # score due to capsules
        
        capsules = successorGameState.getCapsules()
        capsuleScore = 0
        capsule_minsofar = 1e10
        if len(capsules) == 0:
            capsule_minsofar = 0
        for capsule in capsules:
            capsule_minsofar = min(
                capsule_minsofar, manhattanDistance(newPos, capsule))
        capsuleScore = -capsule_minsofar-10*len(capsules)
        return food_score+ghost_score+capsuleScore
        print(successorGameState.getScore())

        # end strategy 1

        return successorGameState.getScore()


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        def minimax(curr_agentIndex, game_state, depth):
            val_action = None
            if (self.depth == depth) or game_state.isWin() or game_state.isLose() or (not game_state.getLegalActions(curr_agentIndex)):
                return self.evaluationFunction(game_state), 0

            if curr_agentIndex == game_state.getNumAgents()-1:
                depth += 1
                next_agentIndex = 0
            else:
                next_agentIndex = curr_agentIndex+1

            for action in game_state.getLegalActions(curr_agentIndex):
                next_value = minimax(next_agentIndex, game_state.generateSuccessor(
                    curr_agentIndex, action), depth)
                if not val_action:
                    val_action = (next_value[0], action)
                else:
                    prev_value = val_action[0]
                    if curr_agentIndex == 0:
                        if next_value[0] > prev_value:
                            val_action = (next_value[0], action)
                    else:
                        if next_value[0] < prev_value:
                            val_action = (next_value[0], action)
            return val_action
        final_val_action = minimax(0, gameState, 0)
        return final_val_action[1]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alpha_beta(curr_agentIndex, game_state, depth, min_val, max_val):
            val_action = None
            if (self.depth == depth) or game_state.isWin() or game_state.isLose() or (not game_state.getLegalActions(curr_agentIndex)):
                return self.evaluationFunction(game_state), 0

            if curr_agentIndex == game_state.getNumAgents()-1:
                depth += 1
                next_agentIndex = 0
            else:
                next_agentIndex = curr_agentIndex+1

            for action in game_state.getLegalActions(curr_agentIndex):
                if not val_action:
                    next_value = alpha_beta(next_agentIndex, game_state.generateSuccessor(
                        curr_agentIndex, action), depth, min_val, max_val)
                    val_action = (next_value[0], action)
                    # next_min_val = val_action[0]
                    # next_max_val = val_action[0]
                    if curr_agentIndex == 0:
                        max_val = max(max_val, val_action[0])
                    else:
                        min_val = min(min_val, val_action[0])
                else:
                    if curr_agentIndex == 0 and val_action[0] > min_val:
                        return val_action
                    # if curr_agentIndex != 0:
                    #    if curr_agentIndex == game_state.getNumAgents()-1 and val_action[0] < max_val:
                    #        return val_action
                    if curr_agentIndex != 0 and val_action[0] < max_val:
                        return val_action
                    next_value = alpha_beta(next_agentIndex, game_state.generateSuccessor(
                        curr_agentIndex, action), depth, min_val, max_val)
                    prev_value = val_action[0]
                    if curr_agentIndex == 0:
                        if next_value[0] > prev_value:
                            val_action = (next_value[0], action)
                        max_val = max(max_val, val_action[0])
                    else:
                        if next_value[0] < prev_value:
                            val_action = (next_value[0], action)
                        min_val = min(min_val, val_action[0])
            return val_action

        final_val_action = alpha_beta(
            0, gameState, 0, float('inf'), float('-inf'))
        # print(final_val_action[0])
        return final_val_action[1]
        # util.raiseNotDefined()


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def exptmax(curr_agentIndex, game_state, depth):
            val_action = None
            if (self.depth == depth) or game_state.isWin() or game_state.isLose() or (not game_state.getLegalActions(curr_agentIndex)):
                return self.evaluationFunction(game_state), 0

            if curr_agentIndex == game_state.getNumAgents()-1:
                depth += 1
                next_agentIndex = 0
            else:
                next_agentIndex = curr_agentIndex+1

            p = 1.0/len(game_state.getLegalActions(curr_agentIndex))
            for action in game_state.getLegalActions(curr_agentIndex):
                next_value = exptmax(next_agentIndex, game_state.generateSuccessor(
                    curr_agentIndex, action), depth)
                if not val_action:
                    if curr_agentIndex == 0:
                        val_action = (next_value[0], action)
                    else:
                        val_action = (p*next_value[0], action)
                else:
                    prev_value = val_action[0]
                    if curr_agentIndex == 0:
                        if next_value[0] > prev_value:
                            val_action = (next_value[0], action)
                    else:
                        val_action = (p*next_value[0]+prev_value, action)
            return val_action
        final_val_action = exptmax(0, gameState, 0)
        return final_val_action[1]
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    ghosts = currentGameState.getGhostStates()
    pacman_position = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    final_eval_score = currentGameState.getScore()

    final_eval_score += -20*(len(capsules))
    final_eval_score += -10*(len(foods))

    for food in foods:
        food_distance = manhattanDistance(pacman_position, food)
        if food_distance < 2:
            final_eval_score += -1*food_distance
        elif food_distance < 6:
            final_eval_score += -0.5*food_distance
        else:
            final_eval_score += -0.25*food_distance

    for ghost in ghosts:
        ghost_distance = manhattanDistance(
            pacman_position, ghost.getPosition())
        if ghost.scaredTimer:
            if ghost_distance < 2:
                final_eval_score += -20*ghost_distance
            else:
                final_eval_score += -8*ghost_distance
        else:
            if ghost_distance < 2:
                final_eval_score += 4*ghost_distance
            elif ghost_distance < 6:
                final_eval_score += 2*ghost_distance
            else:
                final_eval_score += 0.5*ghost_distance

    for capsule in capsules:
        capsule_distance = manhattanDistance(pacman_position, capsule)
        if capsule_distance < 2:
            final_eval_score += -15*capsule_distance
        else:
            final_eval_score += -8*capsule_distance

    return final_eval_score
    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
