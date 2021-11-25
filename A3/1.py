import random
import numpy as np
from collections import defaultdict

'''
	Solving taxi problem with MDP
'''

# states:
# (i1,j1,i2,j2) => taxi at i1,j1 and passenger at i2,j2

# actions:
# actions = [(0,1), (0,-1), (1,0), (-1,0)] # north, south, east and west

# T(s,a,s') =
# transitionArray((1,1,1,1), (0,1), (1,2,1,2)   => 0.85
# transitionArray((1,1,1,1), (0,1), (1,2,1,2)

# reward function:
# R(s,a,s') = R(s')

depots = [(0, 0), (0, 4), (3, 0), (4, 4)]
actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # north, south, east and west
rewards = {}  # reward of states: 4 tuple (i1,j1,i2,j2)
# transition probability of state, action, next state
TransitionArray = defaultdict(int)
values = defaultdict(int)  # value of states
policy = defaultdict(int)  # policy of states
states = []
isInTaxi = False


def valueIteration(problem, epsilon):  # TODO
    # implement value iteration
    # problem = (passengerStart, passengerDestination, taxiStart)
    discount = 0.9
    # convergence criteria: max-norm distance between two consecutive value functions
    while True:
        delta = 0
        for state in states:
            oldValue = values[state]
            newValue = 0
            for action in actions:
                if isSafe(state[0], state[1], state[0] + action[0], state[1] + action[1]):
                    if isInTaxi:
                        nextState = (state[0] + action[0], state[1] + action[1],
                                     state[2] + action[0], state[3] + action[1])
                    else:
                        nextState = (
                            state[0] + action[0], state[1] + action[1], state[0], state[1])
                    currValue = 0
                    for state2 in states:
                        currValue += TransitionArray[state, action, state2] * (
                            rewards[state2] + discount * values[state2])
                    if currValue > newValue:
                        newValue = currValue
                        policy[state] = action
            values[state] = newValue
            delta = max(delta, abs(oldValue - newValue))
        if delta < epsilon:
            break
    print(values)


def policyIteration():  # TODO
    pass


def isSafe(oldx, oldy, newx, newy):
    if(newx >= 0 and newx <= 4 and newy >= 0 and newy <= 4):
        return True
    # walls between [(0,0),(0,1)], [(0,1),(1,1)], [(2,0),(3,1)],[(2,1),(3,1)], [(1,4),(2,4)], [(1,3),(2,3)]
    if (oldx, oldy) == (0, 0) and (newx, newy) == (0, 1):
        return False
    if (oldx, oldy) == (0, 1) and (newx, newy) == (1, 1):
        return False
    if (oldx, oldy) == (2, 0) and (newx, newy) == (3, 1):
        return False
    if (oldx, oldy) == (2, 1) and (newx, newy) == (3, 1):
        return False
    if (oldx, oldy) == (1, 4) and (newx, newy) == (2, 4):
        return False
    if (oldx, oldy) == (1, 3) and (newx, newy) == (2, 3):
        return False
    return True


def addToTransitionArray(state, desiredAction):
    for action in actions:
        newX = state[0] + action[0]
        newY = state[1] + action[1]
        if(isSafe(state[0], state[1], newX, newY)):
            state1 = (newX, newY, state[2], state[3])
            if(action == desiredAction):
                TransitionArray[state, action, state1] = 0.85
            else:
                TransitionArray[state, action, state1] = 0.05
        else:
            TransitionArray[state, action, state] = 1


# transition function
def initTransitionFunction():
    global states
    x = 0
    for i1 in range(5):
        for j1 in range(5):
            for i2 in range(5):
                for j2 in range(5):
                    state = (i1, j1, i2, j2)
                    states += [state]
                    rewards[state] = 0
                    policy[state] = random.choice(actions)
                    values[state] = 0
                    for action in actions:
                        addToTransitionArray(state, action)


def initReward(passengerDestination):
    rewards[passengerDestination] = 1


# def takeAction(taxiLocation, desiredAction):
#     actionTaken =
#     (newX, newY) = taxiLocation + action
#     if(isSafe(taxiLocation[0], taxiLocation[1], newX, newY)):
#         taxiLocation = (newX, newY)
#     return taxiLocation


def simulate():

    # randomly generate starting depot for passenger, select different destination depot for passenger and starting location for taxi
    passengerStart = depots[random.randint(0, 3)]
    depots.remove(passengerStart)
    passengerDestination = depots[random.randint(0, 2)]
    taxiStart = (random.randint(0, 4), random.randint(0, 4))
    print(passengerStart, passengerDestination, taxiStart)
    depots.append(passengerStart)
    isPassengerInTaxi = False

    # initialize reward function
    initReward(passengerDestination)
    initTransitionFunction()

    problem = (passengerStart, passengerDestination, taxiStart)
    valueIteration(problem, 0.001)


if __name__ == '__main__':
    simulate()
    # print(TransitionArray)
