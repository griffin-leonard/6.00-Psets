# 6.0002 Problem Set 2
# Graph optimization
# Name: Griffin Leonard
# Collaborators: n/a
# Time: 6:00

#
# Finding shortest paths through the Boston t
#


import unittest
from graph import Digraph, Node, WeightedEdge


# PROBLEM 2: Building up the Boston t Map
#
# PROBLEM 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the times
# represented?
#
# ANSWER: nodes represent train stations, edges represent the travel time between stations



# PROBLEM 2b: Implementing load_map
def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following format, separated by blank spaces:
            From To TotalTime LineColor
        e.g.
            green_st forest_hills 3 orange
        This entry would become an edge from green_st to forest_hills on the orange line. There should also be
        another edge from forest_hills to green_st on the orange line with time travelled = 3

    Returns:
        a directed graph representing the map
    """
    file = open(map_filename,'r')
    
    graph = Digraph()
    for line in file:
        #get data from file line
        data = line.split()
        node1 = Node(data[0])
        node2 = Node(data[1])
        
        #add data to the digraph
        if not graph.has_node(node1):
            graph.add_node(node1)
        if not graph.has_node(node2):
            graph.add_node(node2)
        graph.add_edge(WeightedEdge(node1,node2,data[2],data[3]))
        graph.add_edge(WeightedEdge(node2,node1,data[2],data[3])) #can travel both directions
        
    return graph



# PROBLEM 2c: Testing load_map
# Include the lines used to test load_map below, but comment them out
#
#print(load_map('test_load_map.txt'))

# PROBLEM 3: Finding the Shortest Path using Optimized Search Method
#
# PROBLEM 3a: Objective function
#
# What is the objective function for this problem? What are the constraints?
#
# ANSWER: The objective funcion is get_best_path and the constraints are
#         the restricted_colors

# PROBLEM 3b: Implement add_node_to_path
    

def add_node_to_path(node, path):
    """
    Parameters:
        path: list composed of [[list of nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of nodes (Node) and total time traveled
    
        node: Node object 
            Node of t stop being added to the path
            
    Returns:
        [[list of nodes], int] - A safely COPIED version of path with the Node added to the end of 
        a COPY of the first element of path.
        
        This method should not mutate path or path[0]
        
    """
    pcopy = [path[0][:],int(path[1])]
    pcopy[0].append(node)
    return pcopy

# PROBLEM 3c: Implement get_best_path
def get_best_path(digraph, start, end, path, restricted_colors, best_time,
                  best_path):
    """
    Finds the shortest path between t stops subject to constraints.

    Parameters:
        digraph: Digraph
            The graph on which to carry out the search
        start: Node
            t stop at which to start
        end: Node
            t stop at which to end
        path: list composed of [[list of Nodes], int]
            Represents the current path of nodes being traversed. Contains
            a list of Nodes and total time traveled.
        restricted_colors: list[strings]
            Colors of lines not allowed on path
        best_time: int
            The shortest time between the original start and end node
            for the initial problem that you are trying to solve
        best_path: list of Nodes
            The path with the shortest total time found so far between the original start
            and end node.

    Returns:
        A tuple of the form (best_path, best_time).
        The first item is the shortest-path from start to end, represented by
        a list of t stops (Nodes).
        The second item is an integer, the length (time traveled)
        of the best path.
        

        If there exists no path that satisfies restricted_colors constraints, then return None.
    """
    #test if start and end are valid nodes
    if not(digraph.has_node(start) or digraph.has_node(end)):
        raise ValueError('start and/or end is not a valid node')
        
    #if start and end are the same node, the best path has been found
    elif start == end:
        best_time = path[1]
        best_path = path[0]
        
    else:
        for edge in digraph.get_edges_for_node(start):
            #tests to make sure no restricted colors are used and avoids looping
            if edge.get_color() not in restricted_colors and edge.get_destination() not in path[0]:
                #adds the next node to the path and updates the total time (path[1])
                newPath = add_node_to_path(edge.get_destination(),path)
                newPath[1] += edge.get_total_time()
                if best_path == None or best_time > newPath[1]:
                    #creates a new path starting 
                    aPath = get_best_path(digraph,edge.get_destination(),end,\
                                newPath,restricted_colors,best_time,best_path)
                    #only update the best path and time 
                    #if aPath successfully reaches the end node
                    if aPath != None:
                        best_path = aPath[0]
                        best_time = aPath[1]
    
    #returns None if a path from current node to end node doesn't exist        
    if best_path != None:
        return (best_path,best_time)
    else:
        return None
                

### USED FOR TESTING. PLEASE DO NOT CHANGE THIS FUNCTION.
def directed_dfs(digraph, start, end, restricted_colors):
    """
    Finds the shortest time path from start to end using a directed depth-first
    search. Minimize the total time and do not use the color lines in colors_not_used.

    Parameters:
        digraph: instance of Digraph
            The graph on which to carry out the search
        start: Node
            t-stop at which to start
        end: Node
            t-stop at which to end
        restricted_colors: list[string]
            Colors of lines not allowed in path

    Returns:
        The shortest-path from start to end, represented by
        a list of t stops (Nodes).

        If there exists no path that satisfies restricted_colors constraints, then raises a ValueError.
    """
    path = [[start], 0]  # begin at start node with 0 distance
    result = get_best_path(digraph, start, end, path, restricted_colors, 99999, None)
    
    if result is None:
        raise ValueError("No path from {} to {}".format(start, end))
    
    return result[0]


#UNCOMMENT THE FOLLOWING LINES TO DEBUG IF YOU WOULD LIKE TO    

#digr = load_map('t_map.txt')
#
#start = Node('central')
#end = Node('park_st')
#restricted_colors = []
#
#print(directed_dfs(digr, start, end, restricted_colors))


