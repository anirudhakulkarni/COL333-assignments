# Automated-Nurse-Rostering-System
# problem is expressed as search tree
import csv
import sys
import json
import copy
import sys
import time
sys.setrecursionlimit(2500)

''' Backtracing search for constraint satisfaction problem'''


class Node():
    '''
    Node is a class that represents a day nurse combination. Each node has a day, a shift, and a nurse.
    '''

    def __init__(self, day, nurse, shift_arr):
        self.day = day
        self.shift = None
        self.nurse = nurse
        self.domains_available = copy.deepcopy(shift_arr)
        self.isFinal = False
        self.edges = []

    def __str__(self):
        return str(self.day) + " " + str(self.nurse) + " " + str(self.shift)


class Problem():
    '''
    External search space graph. Contains graph of states and methods to traverse it.
    Methods:
        1. check_validity: checks if the problem is valid
        2. solve: solves the problem using AC-3 algorithm
    '''

    def __init__(self, total_nurses, total_days, m, a, e, shift_arr):
        self.total_nurses = total_nurses
        self.total_days = total_days
        self.m = m  # m
        self.a = a  # a
        self.e = e  # e
        self.total_count = {"M": m, "A": a, "E": e}
        self.shift_array = shift_arr
        self.nodes = []
        #self.edges = {}
        for i in range(self.total_days):
            for j in range(self.total_nurses):
                new_node = Node(i, j, self.shift_array)
                self.nodes.append(new_node)

        for i in range(self.total_days-1):
            for j in range(self.total_nurses):
                self.nodes[i*self.total_nurses +
                           j].edges.append(self.nodes[(i+1)*self.total_nurses+j])

    def check_validity(self):
        # check if the problem is valid
        if self.total_nurses-self.m-self.e < self.m:
            return False
        if self.total_nurses < 1 or self.total_days < 1 or self.m < 1 or self.a < 1 or self.e < 1:
            return False
        if self.m+self.a+self.e > self.total_nurses:
            return False
        if self.m+self.a+self.e == self.total_nurses and self.total_days >= 7:
            return False
        return True

    def constraint_satisfied(self, node1, node2, i):
        if(i == "M"):
            da_n1 = node1.domains_available
            if(len(da_n1) == 1 and (da_n1[0] == i or da_n1[0] == "E")):
                return False
            elif(len(da_n1) == 2 and da_n1[0] == i and da_n1[1] == "E"):
                return False
        return True

    def get_domain(self, node):
        # a+r=m : domain=[m]
        if self.a+self.total_nurses-self.a-self.m-self.e == self.m:
            return ["M"]
        if self.a+self.total_nurses-self.a-self.m-self.e == self.m+1:
            return ["M", "E"]

        # r+a<m no solution
        # m is reached domain = [a,r]
        # a is reached
        return node.domains_available

    def sol(self):
        sol_dict = {}
        for i in range(self.total_nurses):
            for j in range(self.total_days):
                sol_dict["N"+str(i)+"_"+str(j)] = self.nodes[i +
                                                             (j*self.total_nurses)].shift
        return sol_dict

    def backtracking_simpler(self,):
        ''' Backtracing search for constraint satisfaction problem'''
        # create a stack
        stack = []
        # create a root node
        root = Node(0, 0, self.shift_array)
        # push root to the stack
        stack.append(root)
        # while stack is not empty
        while len(stack) > 0:
            # pop a node from the stack
            node = stack.pop()
            # if node is a leaf node
            if node.isFinal:
                # return solution
                return self.sol()
            # get the domain of the node
            domain = self.get_domain(node)
            # for each value in the domain
            for value in domain:
                # create a new node
                new_node = Node(node.day, node.nurse, self.shift_array)
                # set the value of the new node
                new_node.shift = value
                # push the new node to the stack
                stack.append(new_node)


if __name__ == "__main__":
    # take input from csv file from argument 1
    # nurses, days, mornings, afternoons, evenings
    try:
        filename = sys.argv[1]
    except:
        filename = "input_a.csv"
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        row_list = []
        for row in reader:
            row_list.append(row)
        row_list = row_list[1:]
        roaster_solution_list = []
        for row in row_list:
            nurses = int(row[0])
            days = int(row[1])
            mornings = int(row[2])
            afternoons = int(row[3])
            evenings = int(row[4])
            roaster = Problem(nurses, days, mornings,
                              afternoons, evenings, ["M", "A", "E", "R"])
            if roaster.check_validity():
                a = set()
                t1 = time.time()
                sol_exist = roaster.backtracking_simpler()
                t2 = time.time()
                print("Time taken for search: ", t2-t1)
                if(sol_exist):
                    t3 = time.time()
                    print("Time taken for solutionexists:", t3-t2)
                    roaster_solution = roaster.sol()
                    t4 = time.time()
                    print("Time taken for sol:", t4-t3)
                else:
                    # roaster_solution = {"NO-SOLUTION": -1}
                    roaster_solution = {}
            else:
                # roaster_solution = {"NO-SOLUTION": -1}

                roaster_solution = {}
            print(roaster_solution)
            roaster_solution_list.append(roaster_solution)
            # save roaster solution in json file

        with open('solution.json', 'w') as outfile:
            for d in roaster_solution_list:
                json.dump(d, outfile)
                outfile.write('\n')
