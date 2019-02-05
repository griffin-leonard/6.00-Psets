# 6.0002 Problem Set 2
# Graph Optimization
# Name: Griffin Leonard
# Collaborators: n/a
# Time: 2:00

#
# A set of data structures to represent the graphs that you will be using for this pset.
#

class Node(object):
    """Represents a node in the graph"""
    def __init__(self, name):
        self.name = str(name)

    def get_name(self):
        ''' return: the name of the node '''
        return self.name

    def __str__(self):
        ''' return: The name of the node.
                This is the function that is called when print(node) is called.
        '''
        return self.name

    def __repr__(self):
        ''' return: The name of the node.
                Formal string representation of the node
        '''
        return self.name

    def __eq__(self, other):
        ''' returns: True is self == other, false otherwise
                 This is function called when you used the "==" operator on nodes
        '''
        return self.name == other.name

    def __ne__(self, other):
        ''' returns: True is self != other, false otherwise
                This is function called when you used the "!=" operator on nodes
        '''
        return not self.__eq__(other)

    def __hash__(self):
        ''' This function is necessary so that Nodes can be used as
        keys in a dictionary, Nodes are immutable
        '''
        return self.name.__hash__()


## PROBLEM 1: Implement this class based on the given docstring.
class WeightedEdge(object):
    """Represents an edge with an integer weight"""
    def __init__(self, src, dest, total_time, color):
        """ Initialize  src, dest, total_time, and color for the WeightedEdge class
            src: Node representing the source node
            dest: Node representing the destination node
            total_time: int representing the time travelled between the src and dest
            color: string representing the t line color of the edge
        """
        self.src = src
        self.dest = dest
        self.total_time = int(total_time)
        self.color = color
    
    def get_source(self):
        """ Getter method for WeightedEdge
            returns: Node representing the source node """
        return self.src

    def get_destination(self):
        """ Getter method for WeightedEdge
            returns: Node representing the destination node """
        return self.dest
    
    def get_color(self):
        """ Getter method for WeightedEdge
            returns: String representing the t-line color of the edge"""
        return self.color
    
    def get_total_time(self):
        """ Getter method for WeightedEdge
            returns: int representing the time travelled between the source and dest nodes"""
        return self.total_time
    
    def __str__(self):
        """ to string method
            returns: string with the format 'src -> dest total_time color' """
        return str(self.src.get_name()+' -> '+self.dest.get_name()+' '\
                   +str(self.get_total_time())+' '+self.get_color())


## PROBLEM 1: Implement methods of this class based on the given docstring.
## DO NOT CHANGE THE FUNCTIONS THAT HAVE BEEN IMPLEMENTED FOR YOU.
class Digraph(object):
    """Represents a directed graph of Node and WeightedEdge objects"""
    def __init__(self):
        self.nodes = set([])
        self.edges = {}  # must be a dictionary of Node -> list of edges starting at that node

    def __str__(self):
        edge_strs = []
        for edges in self.edges.values():
            for edge in edges:
                edge_strs.append(str(edge))
        edge_strs = sorted(edge_strs)  # sort alphabetically
        return '\n'.join(edge_strs)  # concat edge_strs with "\n"s between them

    def get_edges_for_node(self, node):
        ''' param: node object
            return: a copy of the list of all of the edges for given node.
                    empty list if the node is not in the graph
        '''
        return self.edges[node][:]

    def has_node(self, node):
        ''' param: node object
            return: True, if node is in the graph. False, otherwise.
        '''
        if node in self.nodes:
            return True
        return False

    def add_node(self, node):
        """ param: node object
            Adds a Node object to the Digraph.
            Raises a ValueError if it is already in the graph."""
        if node in self.nodes:
            raise ValueError('node already in graph')
        self.nodes.add(node)
        self.edges[node] = []

    def add_edge(self, edge):
        """ param: WeightedEdge object
            Adds a WeightedEdge instance to the Digraph.
            Raises a ValueError if either of the nodes associated with the edge is not in the graph."""
        if not(edge.get_source() in self.nodes and edge.get_destination() in self.nodes):
            raise ValueError('source node and/or destination node does not exist')
        else:
            self.edges[edge.get_source()].append(edge)
