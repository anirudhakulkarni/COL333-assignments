# Automated-Nurse-Rostering-System
# problem is expressed as search tree
import csv
import sys
import json
import copy
sys.setrecursionlimit(4500)


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
        self.back_node = None

    def __str__(self):
        return str(self.day) + " " + str(self.nurse) + " " + str(self.shift)

    '''def assignNurse(self, nurse):
        self.nurse = nurse'''


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
        self.r = self.total_nurses-(self.a+self.m+self.e)
        self.total_count = {"M": m, "A": a, "E": e}
        self.shift_array = shift_arr
        self.nodes = []
        # self.edges = {}
        for i in range(self.total_days):
            for j in range(self.total_nurses):
                new_node = Node(i, j, self.shift_array)
                self.nodes.append(new_node)

        for i in range(self.total_days-1):
            for j in range(self.total_nurses):
                # constraint 2: no nurse works two morning shifts in a row
                # self.edges[self.nodes[i*self.total_nurses+j]] = [self.nodes[(i+1)*self.total_nurses+j], ]
                # self.edges[self.nodes[i*self.total_nurses+j]] = self.nodes[(i+1)*self.total_nurses+j]
                self.nodes[i*self.total_nurses +
                           j].edges.append(self.nodes[(i+1)*self.total_nurses+j])
                self.nodes[(i+1)*self.total_nurses +
                           j].back_node = (self.nodes[i*self.total_nurses+j])

    def check_validity(self):
        # check if the problem is valid
        if self.total_nurses < 1 or self.total_days < 1 or self.m < 1 or self.a < 1 or self.e < 1:
            return False
        if self.m+self.a+self.e > self.total_nurses:
            return False
        if self.m+self.a+self.e == self.total_nurses and self.total_days >= 7:
            return False
        return True

    '''def ac3(self, node_changed):
        queue = []
        for node1 in self.edges:
            for node2 in self.edges[node1]:
                queue.append((node1, node2))
        while len(queue) > 0:
            node1, node2 = queue.pop(0)
            if self.revise(node1, node2):
                if len(node1.domains_available) == 0:
                    return False
                for node3 in self.edges[node1]:
                    if node3 != node2:
                        queue.append((node3, node1))
        return True'''

    def ac(self, node1):
        # a+r==m then left a or r then only M else
        # count = 0
        if(len(node1.edges) > 0):
            node2_ = node1.edges[0]
            if(node2_.day % 7 == 6):
                is_r = False
                curr_node = copy.copy(node2_)
                curr_node = curr_node.back_node
                for i in range(6):
                    if(curr_node.shift == "R"):
                        is_r = True
                        break
                    if(i < 5):
                        curr_node = curr_node.back_node
                if(is_r == False):
                    node2_.domains_available = ["R"]
                    return True
        queue = []
        if(len(node1.edges) == 0):
            return True
        for node2 in node1.edges:
            queue.append((node1, node2))
        # queue.append((node1, self.edges[node1]))

        while(len(queue) > 0):
            # count += 1
            n1, n2 = queue.pop(0)
            if(self.revise(n1, n2)):
                if(len(n2.domains_available) == 0):
                    return False
                for node3 in node2.edges:
                    queue.append((node2, node3))
                # queue.append((n2, self.edges[n2]))
        # print(count)
        return True

    def constraint_satisfied(self, node1, node2, i):
        if(i == "M"):
            da_n1 = node1.domains_available
            if(len(da_n1) == 1 and (da_n1[0] == i or da_n1[0] == "E")):
                return False
            elif(len(da_n1) == 2 and ((da_n1[0] == i and da_n1[1] == "E") or (da_n1[0] == "E" and da_n1[1] == i))):
                return False
        return True

    def revise(self, node1, node2):
        revised = False
        da_n1 = node1.domains_available
        if(self.a+self.r == self.m):
            if(len(da_n1) == 1 and (da_n1[0] == "A" or da_n1[0] == "R")):
                node2.domains_available = ["M"]
                revised = True
                return revised
            if(len(da_n1) == 1 and ((da_n1[0] == "A" and da_n1[1] == "R") or (da_n1[0] == "R" and da_n1[1] == "A"))):
                node2.domains_available = ["M"]
                revised = True
                return revised
        for i in node2.domains_available:
            if not self.constraint_satisfied(node1, node2, i):
                node2.domains_available.remove(i)
                # print("r")
                revised = True
        return revised

    '''def backtrack(self, root):
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
        return False'''

    def search(self, p, d, nurse, count, day7_set):
        if(d == p.total_days):
            return True

        # count_old = count
        curr_node = p.nodes[d*self.total_nurses+nurse]
        da = curr_node.domains_available
        # print(da)

        # assigning shift from available shift
        if(len(da) == 0):
            return False
        # print(d, nurse, da)
        for val in da:
            if(val == "R" or count[val] < self.total_count[val]):
                p_new = copy.deepcopy(p)
                curr_node = p_new.nodes[d*self.total_nurses+nurse]
                curr_node.shift = val
                curr_node.domains_available = [val, ]

                # running ac3
                flag = p_new.ac(curr_node)

                # flag = True
                if flag:
                    d_new = copy.copy(d)
                    nurse_new = copy.copy(nurse)
                    count_new = copy.deepcopy(count)
                    day7_set_new = copy.deepcopy(day7_set)
                    if(val == "R"):
                        day7_set_new.add(nurse)
                    flag3 = True
                    if(nurse_new == self.total_nurses-1):
                        d_new += 1
                        if(d_new != 0 and d_new % 7 == 0):
                            if(len(day7_set_new) == self.total_nurses):
                                day7_set_new = set()
                            else:
                                flag3 = False
                        count_new["M"] = 0
                        count_new["A"] = 0
                        count_new["E"] = 0
                    elif(val != "R"):
                        count_new[val] += 1
                    nurse_new = (nurse_new+1) % self.total_nurses
                    if(flag3):
                        flag2 = self.search(
                            p_new, d_new, nurse_new, count_new, day7_set_new)
                        if(flag2):
                            '''if(d_new%7 == 0):
                                .check_week()'''
                            node_to_update = self.nodes[d *
                                                        self.total_nurses+nurse]
                            node_to_update.isFinal = True
                            node_to_update.shift = val
                            # print(da)
                            # print(d, nurse, val)
                            return True
        return False

    def sol(self):
        sol_dict = {}
        for i in range(self.total_nurses):
            for j in range(self.total_days):
                sol_dict["N"+str(i)+"_"+str(j)] = self.nodes[i +
                                                             (j*self.total_nurses)].shift
        return sol_dict


if __name__ == "__main__":
    # take input from csv file from argument 1
    # nurses, days, mornings, afternoons, evenings
    try:
        filename = sys.argv[1]
    except:
        filename = "input_a.csv"
    with open("solution.json", "a") as jsonfile:
        # clear contents of the file
        jsonfile.truncate(0)
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
                              afternoons, evenings, ["A", "E", "M", "R"])
            if roaster.check_validity():
                a = set()
                sol_exist = roaster.search(
                    roaster, 0, 0, {"M": 0, "A": 0, "E": 0}, a)
                if(sol_exist):
                    roaster_solution = roaster.sol()
                else:
                    roaster_solution = {}
            else:
                roaster_solution = {}
            print(roaster_solution)
            roaster_solution_list.append(roaster_solution)
            # append roaster solution in json file
            with open("solution.json", "a") as jsonfile:
                json.dump(roaster_solution, jsonfile)
                jsonfile.write("\n")
