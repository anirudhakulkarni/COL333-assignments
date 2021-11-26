import random
import numpy as np

NORTH = 0
SOUTH = 1
EAST = 2
WEST = 3
PICKUP = 4
PUTDOWN = 5



depots = [(0, 0), (0, 4), (3, 0), (4, 4)]

q = {}
def initialise():
	for i1 in range(5):
		for j1 in range(5):
			for i2 in range(5):
				for j2 in range(5):
					for a1 in range(6):
						state1 = (i1,j1,i2,j2,True)
						state2 = (i1,j1,i2,j2,False)
						q[state1,a1] = 0
						q[state2,a1] = 0



# s(a,b,c,d,e) => a,b taxi c,d banda, e hai true
						

def reward(s,a,sPrime,dest):

	if(s[0]==sPrime[0]==s[2]==sPrime[2]==dest[0] and s[1]==sPrime[1]==s[3]==sPrime[3]==dest[1] and a==PUTDOWN and s[4] and not sPrime[4]):
		return 20

	elif((a==PICKUP or a==PUTDOWN) and (s[0]!=s[2] or s[1]!=s[3])):
		return -10
	else:
		return -1



def isSafe(newx, newy):
    if(newx >= 0 and newx <= 4 and newy >= 0 and newy <= 4):
        return True
    return False





def epsilon(degrading, i):
	x = random.random()
	if(degrading):
		return x< 0.1/i
	else:
		return x<0.1


def q_learning(alpha, gamma,dest,degrading):
	totalReward = 0
	gammaPrime = 1
	s = (random.randint(0,4),random.randint(0,4),random.randint(0,4),random.randint(0,4),False)
	for i in range(500):
		if(s[2]==dest[0] and s[3]==dest[1] and s[4] == False):
			return
		else:
			sPrime = (0,0,0,0,False)
			if(epsilon(degrading,i)):
				a = random.randint(0,5)
			else:
				a = 0
				val = q[s,a]
				for action in range(6):
					if(q[s,action]>val):
						val = q[s,action]
						a = action

			
			newTaxiX = s[0]
			newTaxiY = s[1]
			newPersonX = s[2]
			newPersonY = s[3]
			newInTaxi = s[4]
			if(a==PICKUP):
				newInTaxi = True
			elif(a==PUTDOWN):
				newInTaxi = False
			else:
				a = pActions(a)
				if(a==NORTH):
					newTaxiY = s[1] + 1
					if(s[4]):
						newPersonY = s[3] + 1
				if(a==SOUTH):
					newTaxiY = s[1] - 1
					if(s[4]):
						newPersonY = s[3] - 1
				if(a==EAST):
					newTaxiX = s[0] + 1
					if(s[4]):
						newPersonX = s[2] + 1
				if(a==WEST):
					newTaxiX = s[0] - 1
					if(s[4]):
						newPersonX = s[2] - 1
			

			if(isSafe(newTaxiX, newTaxiY) and isSafe(newPersonX,newPersonY)):
				sPrime = (newTaxiX,newTaxiY,newPersonX,newPersonY,newInTaxi)
			else:
				sPrime = s


			q[s,a] = (1-alpha)*q[s,a] + alpha*(reward(s,a,sPrime,dest) + gamma*max(q[sPrime,action] for action in range(6)))


			totalReward = totalReward + gammaPrime*reward(s,a,sPrime,dest)
			gammaPrime = gammaPrime*gamma
			s = sPrime

	return totalReward




def sarsa(alpha,gamma, dest, degrading):
	totalReward = 0
	gammaPrime = 1
	s = (random.randint(0,4),random.randint(0,4),random.randint(0,4),random.randint(0,4),False)

	for i in range(500):
		if(s[2]==dest[0] and s[3]==dest[1] and s[4] == False):
			return
		else:
			sPrime = (0,0,0,0,False)
			aPrime = 0
			if(epsilon(degrading,i)):
				a = random.randint(0,5)
			else:
				a = 0
				val = q[s,a]
				for action in range(6):
					if(q[s,action]>val):
						val = q[s,action]
						a = action

			
			newTaxiX = s[0]
			newTaxiY = s[1]
			newPersonX = s[2]
			newPersonY = s[3]
			newInTaxi = s[4]
			if(a==PICKUP):
				newInTaxi = True
			elif(a==PUTDOWN):
				newInTaxi = False
			else:
				a = pActions(a)
				if(a==NORTH):
					newTaxiY = s[1] + 1
					if(s[4]):
						newPersonY = s[3] + 1
				if(a==SOUTH):
					newTaxiY = s[1] - 1
					if(s[4]):
						newPersonY = s[3] - 1
				if(a==EAST):
					newTaxiX = s[0] + 1
					if(s[4]):
						newPersonX = s[2] + 1
				if(a==WEST):
					newTaxiX = s[0] - 1
					if(s[4]):
						newPersonX = s[2] - 1
			

			if(isSafe(newTaxiX, newTaxiY) and isSafe(newPersonX,newPersonY)):
				sPrime = (newTaxiX,newTaxiY,newPersonX,newPersonY,newInTaxi)
			else:
				sPrime = s

			if(epsilon(degrading,i)):
				aPrime = random.randint(0,5)
			else:
				aPrime = 0
				val = q[sPrime,aPrime]
				for action in range(6):
					if(q[sPrime,action]>val):
						val = q[sPrime,action]
						aPrime = action



			q[s,a] = (1-alpha)*q[s,a] + alpha*(reward(s,a,sPrime,dest) + gamma*(q[sPrime,aPrime]))

			totalReward = totalReward + gammaPrime*reward(s,a,sPrime,dest)
			gammaPrime = gammaPrime*gamma
			s = sPrime

	return totalReward
	


def pActions(a):
	x = random.randint(1,100)
	if(x<=85):
		return a
	elif(x<=90):
		return (a+1)%4
	elif(x<95):
		return (a+2)%4
	else:
		return (a+3)%4



def simulate():
	person = random.choice(depots)
	depots.remove(person)
	destination = (2,2)
	depots.append(person)
	taxi = (random.randint(0, 4), random.randint(0, 4))
	print(taxi, person, destination)
	pInTaxi = False
	print("YO")

	while True:
		if(person==destination and pInTaxi == False):
			return 
		else:
			state = (taxi[0], taxi[1], person[0], person[1], pInTaxi)
			optimal = 0
			val = 0
			for act in range(6):
				if(q[state,act]>val):
					val = q[state,act]
					optimal = act

			print("Action:", end = "")
			print(optimal)
			print(taxi)
			print(person)

			if(optimal==PICKUP):
				pInTaxi = True
			elif(optimal==PUTDOWN):
				pInTaxi = False
			else:
				optimal = pActions(optimal)
				newTaxiX = taxi[0]
				newTaxiY = taxi[1]
				newPersonX = person[0]
				newPersonY = person[1]
				if(optimal==NORTH):
					newTaxiY = taxi[1] + 1
					if(pInTaxi):
						newPersonY = person[1] + 1
				if(optimal==SOUTH):
					newTaxiY = taxi[1] - 1
					if(pInTaxi):
						newPersonY = person[1] - 1
				if(optimal==EAST):
					newTaxiX = taxi[0] + 1
					if(pInTaxi):
						newPersonX = person[0] + 1
				if(optimal==WEST):
					newTaxiX = taxi[0] - 1
					if(pInTaxi):
						newPersonX = person[0] - 1

			if(isSafe(newTaxiX,newTaxiY) and isSafe(newPersonX,newPersonY)):
				taxi = (newTaxiX,newTaxiY)
				person = (newPersonX,newPersonY)



if __name__ == '__main__':
	alpha = 0.25
	gamma = 0.99
	initialise()
	for x in range(2000):
		print(x)
		destination = (2,2)
		degrading = False
		sarsa(alpha, gamma,destination,degrading)
		totalRewardList = []
		for i in range(10):
			sarsa()




	for i1 in range(5):
		for j1 in range(5):
			for i2 in range(5):
				for j2 in range(5):
					state1 = (i1,j1,i2,j2,True)
					print(state1, end = ": ")
					a = 0
					val = q[state1,0]
					for action in range(6):
						if(q[state1,action]>val):
							val = q[state1,action]
							a = action
					print(a, end = ", ")
					print(val)
					state2 = (i1,j1,i2,j2,False)
					print(state2, end = ": ")
					a = 0
					val = q[state2,0]
					for action in range(6):
						if(q[state2,action]>val):
							val = q[state2,action]
							a = action
					print(a, end = ", ")
					print(val)
	simulate()




