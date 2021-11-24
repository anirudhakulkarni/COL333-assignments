import random
def prob(): # function to return true with probability = 0.85
	x = random.randint(1,100)
	return x<=85



actions = [(0,1), (0,-1), (0,1), (0,-1)] # north, south, east and west



def valueIteration():


def policyIteration():

def isSafe(x,y):
	if(x>=0 and x<=5 and y>=0 and y<=5):
		return True
	return False

def addToTransitionArray(state,desiredAction):
	for action in actions:
		newX = state[0] + action[0]
		newY = state[1] + action[1]
		if(isSafe(newX, newY)):
			state1 = (newX, newY,state[2], state[3])
			if(action==desiredAction):
				addToTransitionArray(state,action,state1) = 0.85
			else:
				addToTransitionArray(state,action,state1) = 0.05

		else:
			addToTransitionArray(state,action,state) = 1


transitionArray = {}
hashMapForStates = {}
x = 0
for i1 in range(5):
	for j1 in range(5):
		for i2 in range(5):
			for j2 in range(5):
				hashMapForStates[state] = x
				x = x + 1
				addToTransitionArray(state,(0,1))
				addToTransitionArray(state,(0,-1))
				addToTransitionArray(state,(1,0))
				addToTransitionArray(state,(-1,0))



values = [0 for i in range 625]









if __name__ == '__main__':
	start()










