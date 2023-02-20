import sys
from timeit import default_timer as timer

class Node:
    """
    This is a class designed to hold the data for each of the nodes in the graph

    Atributes:
        self.x_coord - x coordinate of the node
        self.y_coord - y coordinate of the node
        self.neighbours - a list of node objects
        self.visited - holds whether or not the node has been visited
    """

    def __init__(self, x_coord:int, y_coord:int):
        """
        Method used to initialise a node

        Parameters:
            self - the current node
            x_coord - the x_coordinate of the node to add to neighbours
            y_coord - the y_coordinate of the node to add to neighbours

        Returns:
            No return values
        """
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.neighbours = []
        self.visited = False

    def add_neighbour(self, other):
        """
        Method used to add a node to the neighbours

        Parameters:
            self - the current node
            other - the node to be added to neighbours of the current node

        Returns:
            No return values
        """
        if not self.is_neighbour(other):
            self.neighbours.append(other)

    def is_neighbour(self, other)->bool:
        """
        Method used to check if a given node is a neighbour of a current node

        Parameters:
            self - the current node
            other - the node we wish to check for in neighbours

        Returns:
            Whether or not a node is a neighbour of the node
        """
        for node in self.neighbours:
            if node.x_coord == other.x_coord and node.y_coord == other.y_coord:
                return True
        return False

    def is_visited(self)->bool:
        """
        Method used to check if a current node has been visited

        Parameters:
            self - the current node

        Returns:
            Whether or not the current node has been visited
        """
        return self.visited

class Graph:
    """
    This is a class designed to hold the graph for the maze

    Atributes:
        self.nodes - a dictionary linking a tuple containing x, y coordinates to the node for the given x, y position
    """
    
    def __init__(self):
        """
        Method used to initialise a graph

        Parameters:
            self - the current node

        Returns:
            No return values
        """
        self.nodes = {}

    def add_new_node(self, coords:tuple)->Node:
        """
        Method used tp create and add a new node to the graph

        Parameters:
            self - the current node
            coords - a tuple containing the x, y coordinates of the node

        Returns:
            The node added to the graph
        """
        node = Node(coords[0], coords[1])
        self.nodes[coords] = node
        return node

    def get_node(self, coords:tuple)->Node:
        """
        Method used to returns the instance of node with given coordinates

        Parameters:
            self - the current node
            coords - a tuple containing the x, y coordinates of the node

        Returns:
            The node for the given coordinates
        """
        return self.nodes[coords]

#open a file and read the maze into a 2D array
with open("maze-Medium.txt", "r") as maze_file:
    maze_matrix = []        #stores the maze as a 2D array
    lines = maze_file.readlines()
    for line in lines:
        if not line.find("#"):      #removes any lines that contain just newlines
            maze_matrix.append(line.rstrip("\n").rstrip(" ").split(" "))        #generates the 2D array

#used to increase the recursion limit to the prevent program from being incorrectly terminated by maximum recursion depth exceeded error
sys.setrecursionlimit(len(maze_matrix) * len(maze_matrix[0]))

maze_graph = Graph()
display_matrix = []
for line in maze_matrix:
    display_matrix.append(line.copy())

def create_graph(maze_matrix:list):
    """
        Method used to fill a graph object with nodes
        Parameters:
            maze_matrix - represents the maze as a 2D array

        Returns:
            No return values
    """
    maze_width = len(maze_matrix[0])
    maze_height = len(maze_matrix)

    for y in range(maze_width):
        if maze_matrix[0][y] == '-':
            display_matrix[0][y] = "S"
            start_node = maze_graph.add_new_node((0,y))
            
    for x in range(1, maze_height-1):
        for y in range(1,maze_width-1):
            if maze_matrix[x][y] == '-':
                maze_graph.add_new_node((x,y))

    for y in range(maze_width):
        if maze_matrix[maze_height-1][y] == '-':
            display_matrix[maze_height-1][y] = "E"
            end_node = maze_graph.add_new_node((maze_height-1,y))
    
    for node in maze_graph.nodes.values():
        add_neighbours(node)

    return start_node, end_node

def add_neighbours(node:Node):
    """
        Method used to find and add the neighours for the given node to the graph

        Parameters:
            node - the current node

        Returns:
            No return values
    """
    try:
        node.add_neighbour(maze_graph.get_node((node.x_coord-1, node.y_coord)))
    except:
        pass
    try:
        node.add_neighbour(maze_graph.get_node((node.x_coord+1, node.y_coord)))
    except:
        pass
    try:
        node.add_neighbour(maze_graph.get_node((node.x_coord, node.y_coord-1)))
    except:
        pass
    try:
        node.add_neighbour(maze_graph.get_node((node.x_coord, node.y_coord+1)))
    except:
        pass

def display_maze(maze:list):
    """
        Method used to display a maze

        Parameters:
            maze - 2D array representing the maze to be displayed

        Returns:
            No return values
    """
    for line in maze:
        print(" ".join(line))

def dfs_travesal(current_node:Node, goal_node:Node, nodes_explored:int):
    """
        Method used to run dfs on the maze from the current node

        Parameters:
            current_node - the node the algorithm is currently at
            goal_node - the goal node of the dfs algorithm
            nodes_explored - the number of nodes explored by the algorithm

        Returns:
            The path of previous nodes
            nodes_explored - the number of nodes explored by the algorithm
    """
    nodes_explored += 1
    current_node.visited = True
    if current_node == goal_node:
        return [current_node], nodes_explored
    else:
        for neighbour in current_node.neighbours:
            if not neighbour.is_visited():
                dfs_path, nodes_explored = dfs_travesal(neighbour, goal_node, nodes_explored)
                if dfs_path != []:   
                    return [current_node] + dfs_path, nodes_explored
        return [], nodes_explored

start = timer()
start_node, end_node = create_graph(maze_matrix)
path, nodes_explored = dfs_travesal(start_node, end_node, 0)
end = timer()

display_matrix[path[0].x_coord][path[0].y_coord] = 'P'
for node in path[1:-1]:
    display_matrix[node.x_coord][node.y_coord] = 'P'
display_matrix[path[-1].x_coord][path[-1].y_coord] = 'P'

#To show path highlighted in green (Note: wont work when run in terminal)
#display_matrix[path[0].x_coord][path[0].y_coord] = "\033[1;32mS\033[0m"
#for node in path[1:-1]:
#    display_matrix[node.x_coord][node.y_coord] = "\033[1;32mP\033[0m"
#display_matrix[path[-1].x_coord][path[-1].y_coord] = "\033[1;32mE\033[0m"

display_maze(display_matrix)
print("\n==========================\n")
print("Node (%d, %d)" %(start_node.x_coord, start_node.y_coord))
for node in path[1:-1]:
    print("Node (%d, %d)" %(node.x_coord, node.y_coord))
print("Node (%d, %d)" %(end_node.x_coord, end_node.y_coord))
print("\n==========================\n")
print("Nodes explored: %d " %nodes_explored)
print("Time of execution: %f" %(end-start))
print("Path length: %d" %len(path))
