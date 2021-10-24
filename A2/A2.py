# Automated-Nurse-Rostering-System
# problem is expressed as search tree
import csv
import sys
import json


class Node():
    '''
    Node is a class that represents a day shift combination. Each node has a day, a shift, and a nurse.
    '''

    def __init__(self, day, shift, total_nurses):
        self.day = day
        self.shift = shift
        self.nurse = None
        self.domains_available = [i for i in range(total_nurses)]
        self.isFinal = False

    def __str__(self):
        return str(self.day) + " " + str(self.shift) + " " + str(self.nurse)

    def assignNurse(self, nurse):
        self.nurse = nurse


class Problem():
    '''
    External search space graph. Contains graph of states and methods to traverse it.
    Methods:
        1. check_validity: checks if the problem is valid
        2. solve: solves the problem using AC-3 algorithm
    '''

    def __init__(self, total_nurses, total_days, total_mornings, total_afternoons, total_evenings):
        self.total_nurses = total_nurses
        self.total_days = total_days
        self.total_mornings = total_mornings
        self.total_afternoons = total_afternoons
        self.total_evenings = total_evenings
        self.nodes = []
        self.edges = {}
        for i in range(self.total_days):
            n1 = Node(i, 0, self.total_nurses)
            n2 = Node(i, 1, self.total_nurses)
            n3 = Node(i, 2, self.total_nurses)
            self.nodes.append(n1)
            self.nodes.append(n2)
            self.nodes.append(n3)
            # constraint 1: each nurse works at most one shift per day
            self.edges[n1] = [n2, n3]
            self.edges[n2] = [n1, n3]
            self.edges[n3] = [n1, n2]
        for i in range(self.total_days-1):
            # constraint 2: no nurse works two morning shifts in a row
            self.edges[self.nodes[i*3]].append(self.nodes[i*3+3])
            # constraint 3: nurse can not work in morning shift if she has worked evening shift previous day
            self.edges[self.nodes[i*3+2]].append(self.nodes[i*3+3])

    def check_validity(self):
        # check if the problem is valid
        if self.total_nurses < 1 or self.total_days < 1 or self.total_mornings < 1 or self.total_afternoons < 1 or self.total_evenings < 1:
            return False
        if self.total_mornings+self.total_afternoons+self.total_evenings > self.total_days:
            return False
        return True

    def backtrack(self, root):
        # backtrack the tree
        if root.data == 0:
            return True
        if root.data == 1:
            return False
        for i in range(self.nurses):
            for j in range(self.days):
                if root.data[i][j] == 0:
                    root.data[i][j] = 1
                    if self.check_validity(root.data):
                        child = Tree(root.data, root)
                        root.add_child(child)
                        self.backtrack(child)
                    root.data[i][j] = 0
        return False

    def AC3(self, root):
        # AC-3 algorithm
        queue = []
        for i in range(self.nurses):
            for j in range(self.days):
                if root.data[i][j] == 0:
                    queue.append((i, j))
        while len(queue) > 0:
            i, j = queue.pop(0)
            for k in range(self.nurses):
                if self.check_validity(root.data, i, j, k):
                    root.data[i][j] = k
                    for l in range(self.days):
                        if root.data[k][l] == 0:
                            queue.append((k, l))
        return root


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
        for row in row_list:
            nurses = int(row[0])
            days = int(row[1])
            mornings = int(row[2])
            afternoons = int(row[3])
            evenings = int(row[4])
            roaster = Problem(nurses, days, mornings, afternoons, evenings)
            if roaster.check_validity():
                roaster_solution = roaster.solve()
            else:
                roaster_solution = [
                    {"N0_0": "R", "N1_0": "R", "N2_0": "A", "N0_1": "R", "N1_1": "M", "N2_1": "E"}]
            # save roaster solution in json file
            with open('solution.json', 'w') as outfile:
                for d in roaster_solution:
                    json.dump(d, outfile)
                    outfile.write('\n')
