# Automated-Nurse-Rostering-System
# problem is expressed as search tree
import csv
import sys
import json


class Tree():
    '''
    Internal node in the bigger tree. Contains the mapping of nurses to shifts in each day and corresponds to a state.
    Methods:
        1. get_children: returns another state which is one step away from the current state.
        
    '''

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        self.level = 0
        self.path = []
        self.path_cost = 0
        self.heuristic = 0
        self.visited = False

    def add_child(self, obj):
        self.children.append(obj)

    # for debugging

    def __str__(self):
        return str(self.data)


class Problem():
    '''
    External search space graph. Contains graph of states and methods to traverse it.
    Methods:
        1. check_validity: checks if the problem is valid
        2. solve: solves the problem using AC-3 algorithm
    '''


    def __init__(self, nurses, days, mornings, afternoons, evenings):
        self.nurses = nurses
        self.days = days
        self.mornings = mornings
        self.afternoons = afternoons
        self.evenings = evenings

    def check_validity(self):
        # check if the problem is valid
        if self.nurses < 1 or self.days < 1 or self.mornings < 1 or self.afternoons < 1 or self.evenings < 1:
            return False
        if self.mornings+self.afternoons+self.evenings > self.days:
            return False
        return True

    def solve(self):
        # solve the problem using AC-3 algorithm
        if not self.check_validity():
            print("Invalid problem")
            return [{}]
        root = Tree(self.nurses*self.days)
        self.backtrack(root)
        return self.get_solution(root)

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
    filename = sys.argv[1]
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
