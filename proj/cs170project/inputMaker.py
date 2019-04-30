import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

def parse_input_size(inputSize, HOME):
    """ Returns strings representing the size, text filename, graph filename, and number of rowdy_groups """

    # small graph
    if inputSize >= 25 and inputSize <= 50:
        size = "small"
        txtFile = os.path.join(HOME, "ourInputs", "small", "parameters.txt")
        graphFile = os.path.join(HOME, "ourInputs", "small", "graph.gml")
        outFile = os.path.join(HOME, "ourOutputs", "small.out")
        num_groups = np.random.randint(0, 100)
    
    # medium graph
    elif inputSize >= 250 and inputSize <= 500:
        size = "medium"
        txtFile = os.path.join(HOME, "ourInputs", "medium", "parameters.txt")
        graphFile = os.path.join(HOME, "ourInputs", "medium", "graph.gml")
        outFile = os.path.join(HOME, "ourOutputs", "medium.out")
        num_groups = np.random.randint(0, 1000)
    
    # large graph
    elif inputSize >= 500 and inputSize <= 1000:
        size = "large"
        txtFile = os.path.join(HOME, "ourInputs", "large", "parameters.txt")
        graphFile = os.path.join(HOME, "ourInputs","large", "graph.gml")
        outFile = os.path.join(HOME, "ourOutputs", "large.out")
        num_groups = np.random.randint(0, 2000)

    else:
        print("Invalid Size!")
        return

    return (size, txtFile, graphFile, outFile, num_groups)

def heuristic_optimized(inputSize):
    HOME = os.getcwd()

    size, txtFile, graphFile, outFile, _ = parse_input_size(inputSize, HOME)

    # input

    # make files
    if not os.path.exists(os.path.join(HOME, "ourInputs")):
        os.mkdir(os.path.join(HOME, "ourInputs"))

    f = open(txtFile, "w")
    f2 = open(graphFile, "w")
    g = nx.Graph()

    nodes = []
    for i in range(inputSize):
        nodes.append(str(i))
    g.add_nodes_from(nodes)
    rowdy_groups = list()
    
    # chooses between 1 and inputSize / 4 nodes to be centers of star clusters
    popular_nodes = list(set(np.random.randint(1, inputSize, size=np.random.randint(1, inputSize / 4))))

    # for every node, if it is not popular, add an edge between it and a random popular node
    for i in range(inputSize):
        if i not in popular_nodes:
            g.add_edge(str(i), str(np.random.choice(popular_nodes)))
    
    # add an edge between every pair of popular nodes, and make every pair of popular nodes a rowdy group
    for i in popular_nodes:
        for j in popular_nodes:
            if i < j:
                g.add_edge(str(i), str(j))

    # make a rowdy group out of three popular nodes each
    for _ in range(2 * inputSize):
        rand_nodes = np.random.choice(popular_nodes, size=3, replace=False)
        rowdy_groups.append([str(rand_nodes[0]), str(rand_nodes[1]), str(rand_nodes[2])])

    '''
    # show plot, not mandatory
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw(g, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(g, pos=nx.spring_layout(g), edge_labels=labels)
    plt.show()
    '''

    # set bus lengths
    num_buses = len(popular_nodes)
    bus_capacity = (inputSize // num_buses) + 1

    # find optimal bus capacity
    for i in popular_nodes:
        neighbors = list(g.neighbors(str(i)))
        if len(neighbors) > bus_capacity:
            bus_capacity = len(neighbors)
    
    # write the file
    f.write(str(num_buses) + "\n")
    f.write(str(bus_capacity) + "\n")
    for group in rowdy_groups:
        f.write(str(group) + "\n")

    # write gml
    nx.write_gml(g, graphFile)

    # output

    # make files
    if not os.path.exists(os.path.join(HOME, "ourOutputs")):
        os.mkdir(os.path.join(HOME, "ourOutputs"))

    f3 = open(outFile, "w")

    student_on_bus = []
    bus_assignments = list()   
    #print(len(popular_nodes), "POPULAR NODES", popular_nodes)

    # get bus assignments from unpopular neighbors of popular nodes
    for i in popular_nodes:
        bus = []
        if i not in bus:
            bus.append(str(i))
            student_on_bus.append(str(i))
        neighbors = list(g.neighbors(str(i)))
        #print(i, "has", len(neighbors), "NEIGHBORS", neighbors)

        for neighbor in neighbors:
            if int(neighbor) not in popular_nodes:
                if neighbor not in student_on_bus: 
                    bus.append(neighbor)
                    student_on_bus.append(neighbor)
        bus_assignments.append(bus)

    onBus = 0
    for bus in bus_assignments:
        onBus += len(bus)
    #print(onBus, "ON BUS:", student_on_bus)

    # write the file
    for bus in bus_assignments:
        f3.write(str(bus) + "\n")

if __name__ == '__main__':
    # manually testing   
    heuristic_optimized(50)
    heuristic_optimized(500)
    heuristic_optimized(1000)
    print("DONE")