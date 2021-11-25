import random


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
rewards = {}
TransitionArray = {}
values = [0 for i in range(625)]  # value iteration array


def valueIteration(problem, epsilon):  # TODO


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


# hashMapForStates = {}
# x = 0

# transition function
def initTransitionFunction():
    for i1 in range(5):
        for j1 in range(5):
            for i2 in range(5):
                for j2 in range(5):
                    state = (i1, j1, i2, j2)
                    # hashMapForStates[state] = x
                    # x = x + 1
                    addToTransitionArray(state, (0, 1))
                    addToTransitionArray(state, (0, -1))
                    addToTransitionArray(state, (1, 0))
                    addToTransitionArray(state, (-1, 0))


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
