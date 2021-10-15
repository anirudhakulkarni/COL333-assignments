# Automated-Nurse-Rostering-System
# problem is expressed as search tree
import csv
import sys
import json


class Tree():
    # Tree classs for tree
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
        return [{}]

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
