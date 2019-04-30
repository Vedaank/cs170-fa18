import networkx as nx
import os
import time
import random
import copy
from multiprocessing import Pool

HOME = os.getcwd()

###########################################
# Change this variable to the path to 
# the folder containing all three input
# size category folders
###########################################
path_to_inputs = os.path.join(HOME, "inputs")

###########################################
# Change this variable if you want
# your outputs to be put in a 
# different folder
###########################################
# make files
if not os.path.exists(os.path.join(HOME, "outputs")):
    os.mkdir(os.path.join(HOME, "outputs"))
path_to_outputs = os.path.join(HOME, "outputs")

def parse_input(folder_name):
    '''
        Parses an input and returns the corresponding graph and parameters

        Inputs:
            folder_name - a string representing the path to the input folder

        Outputs:
            (graph, num_buses, size_bus, constraints)
            graph - the graph as a NetworkX object
            num_buses - an integer representing the number of buses you can allocate to
            size_buses - an integer representing the number of students that can fit on a bus
            constraints - a list where each element is a list vertices which represents a single rowdy group
    '''
    graph = nx.read_gml(os.path.join(folder_name, "graph.gml"))
    parameters = open(os.path.join(folder_name, "parameters.txt"))
    num_buses = int(parameters.readline())
    size_bus = int(parameters.readline())
    constraints = []
    
    for line in parameters:
        line = line[1: -2]
        curr_constraint = [num.replace("'", "") for num in line.split(", ")]
        constraints.append(curr_constraint)

    return graph, num_buses, size_bus, constraints

def intersection(lst1, lst2): 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3

# Returns True if this student can go in this bus (no rowdy group made), False if otherwise
def rowdy_check(this_student, bus, constraints):
    checker_bus = copy.deepcopy(bus)
    for rowdy_group in constraints:
        if this_student in rowdy_group:
            checker_bus.append(this_student)
            if set(intersection(checker_bus, rowdy_group)) == set(rowdy_group):
                return False
    return True

def solve(graph, num_buses, size_bus, constraints, output_category_path, input_name):
    graph.remove_edges_from(graph.selfloop_edges())
    
    # buses, with bus assignments
    buses = list()

    # list of students who are on a bus already
    students_on_bus = list()
    
    # load students/number of friends as tuple into list
    num_students = graph.number_of_nodes()
    student_friendliness = list()
    for student in list(graph.nodes):
        student_friendliness.append((student, graph.degree[student]))

    # sort student by number of friends, comverting dictionary to list of tuples
    student_friendliness.sort(key=lambda tup: tup[1], reverse=True)

    # put the student with the most friends on their own bus
    for i in range(num_buses):
        bus = list()
        bus.append(student_friendliness.pop(0)[0])
        buses.append(bus)

    # get all the friends of the students not yet assigned
    for s in range(len(student_friendliness)):
        friends = list(graph.adj[student_friendliness[s][0]])

        # list of all buses not yet filled
        unfilled = list()
        for i in range(num_buses):
            if len(buses[i]) < size_bus:
                unfilled.append(i)

        bus_with_most_friends = unfilled[0]
        most_friends = 0
        
        # find bus with most friends of this student
        for i in range(num_buses):
            if len(buses[i]) < size_bus and rowdy_check(student_friendliness[s][0], buses[i], constraints):
                num_friends_on_bus = len(intersection(friends, buses[i]))
                if num_friends_on_bus > most_friends:
                    most_friends = num_friends_on_bus
                    bus_with_most_friends = i

        # add this student to bus with most friends
        x = 1
        while not rowdy_check(student_friendliness[s][0], buses[bus_with_most_friends], constraints) and x < len(unfilled):
            bus_with_most_friends = unfilled[x]
            x += 1

        buses[bus_with_most_friends].append(student_friendliness[s][0])
    
    # make solution  
    solution = ""
    for bus in buses:
        solution += str(bus) + "\n"

    output_file = open(os.path.join(output_category_path, input_name + ".out"), "w")
    output_file.write(solution)
    output_file.close()

def main():
    '''
        Main method which iterates over all inputs and calls `solve` on each.
        The student should modify `solve` to return their solution and modify
        the portion which writes it to a file to make sure their output is
        formatted correctly.
    '''
    size_categories = ["small", "medium", "large"]
    if not os.path.isdir(path_to_outputs):
        os.mkdir(path_to_outputs)

    tasks = []

    for size in size_categories:
        category_path = os.path.join(path_to_inputs, size)
        output_category_path = os.path.join(path_to_outputs, size)
        category_dir = os.fsencode(category_path)
        
        if not os.path.isdir(output_category_path):
            os.mkdir(output_category_path)
        for input_folder in os.listdir(category_dir):
            input_name = os.fsdecode(input_folder)
            graph, num_buses, size_bus, constraints = parse_input(os.path.join(category_path, input_name))
            tasks.append((graph, num_buses, size_bus, constraints, output_category_path, input_name))
    
    num_thread = 11
    print("STARTING with", num_thread, "threads")
    start = time.time()
    pool = Pool(num_thread)
    results = [pool.apply_async(solve, t) for t in tasks]
    pool.close()
    pool.join()
    end = time.time()
    print("TIME", num_thread, end - start)

if __name__ == '__main__':
    main()