import sys
from math import sqrt
from timeit import default_timer as timer
from queue import PriorityQueue

class Node:
    """
    This is a class designed to hold the data for each of the nodes in the graph

    Atributes:
        self.x_coord - x coordinate of the node
        self.y_coord - y coordinate of the node
        self.g - the g value for the node
        self.h - the h value for the node
        self.f - the f value for the node
        self.previous_node - the previous node in the path
        self.neighbours - a list of node objects
        self.visited - holds whether or not the node has been visited
        self.node_number - the id of the node
    """

    def __init__(self, x_coord:int, y_coord:int, node_number:int)->None:
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
        self.g = None
        self.h = None
        self.f = None
        self.previous_node = None
        self.neighbours = []
        self.visited = False
        self.node_number = node_number

    def add_neighbour(self, other)->None:
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
    
    def __lt__(self, other)->bool:
        """
        Method used to define comparison between two nodes

        Parameters:
            self - the current node
            other - the other node being compared to

        Returns:
            Whether or not the current node is smaller than the other node
        """
        return(self.f, self.h, self.node_number) < (other.f, other.h, other.node_number)

    def __eq__(self, other)->bool:
        """
        Method used to define comparison between two nodes

        Parameters:
            self - the current node
            other - the other node being compared to

        Returns:
            Whether or not the current node is equal to the other node
        """
        return(self.f, self.h, self.node_number) == (other.f, other.h, other.node_number)

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
        node = Node(coords[0], coords[1], len(self.nodes))
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

#getting user input for the file and which heuristic to use
file_name = input("Enter the file name of the maze you wish to solve: ")
heuristic_choice = input("Enter heuristic choice(manhattan/euclidean): ")
while heuristic_choice.lower() != "manhattan" and heuristic_choice.lower() != "euclidean":
    heuristic_choice = input("The heuristic entered was not an option. Enter heuristic choice(manhattan/euclidean): ")
try:
    #open a file and read the maze into a 2D array
    with open(file_name, "r") as maze_file:
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
except:
    #if the maze entered is not in the current directory will stop the program
    print("The maze file entered was not valid")
    quit()

def create_graph(maze_matrix:list)->None:
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

def add_neighbours(node:Node)->None:
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

def display_maze(maze:list)->None:
    """
        Method used to display a maze

        Parameters:
            maze - 2D array representing the maze to be displayed

        Returns:
            No return values
    """
    for line in maze:
        print(" ".join(line))

def A_star_search(current_node:Node, goal_node:Node)->list:
    """
        Method used to run the A* search algorithm

        Parameters:
            current_node - the current node
            goal_node - the goal node of the search algorithm

        Returns:
            No return values
    """
    #calculating the total nodes explored
    global nodes_explored
    nodes_explored += 1
    #setting current node as visited
    current_node.visited = True
    if current_node != goal_node:
        #checking all unvisited neighbours and updating their g, h and f values
        for neighbour in current_node.neighbours:
            if not neighbour.is_visited():
                new_g, new_h, new_f = calculate_heuristic(current_node, neighbour, goal_node)
                if neighbour in priority_queue.queue:
                    if new_f < neighbour.f:
                        neighbour.g = new_g
                        neighbour.h = new_h
                        neighbour.f = new_f
                        neighbour.previous_node = current_node
                    elif new_f == neighbour.f:
                        if new_g < neighbour.g:
                            neighbour.g = new_g
                            neighbour.h = new_h
                            neighbour.f = new_f
                            neighbour.previous_node = current_node
                else:
                    #adding neighbouring node to the priority queue if not already on there
                    neighbour.g = new_g
                    neighbour.h = new_h
                    neighbour.f = new_f
                    neighbour.previous_node = current_node
                    priority_queue.put(neighbour, new_f)
        #popping the next node to visit of the priority queue
        next_node = priority_queue.get()
        #recursive call on A* search
        A_star_search(next_node, goal_node)   

def calculate_heuristic(previous_node:Node, current_node:Node, goal_node:Node):
    """
        Method used to caluclate the heuristics for a given node

        Parameters:
            previous_node - the previous node in the path
            current_node - the current node
            goal_node - the goal node of the search

        Returns:
            new_g - the newly calculated g value
            new_h - the newly calculated h value
            new_f - the newly calculated f value
    """
    new_g = previous_node.g + 1
    if heuristic_choice.lower() == "manhattan":
        #calculating the manhattan distance
        new_h = abs(current_node.x_coord - goal_node.x_coord) + abs(current_node.y_coord - goal_node.y_coord)
    
    elif heuristic_choice.lower() == "euclidean":
        #calculating the euclidean distance
        new_h = sqrt((current_node.x_coord-goal_node.x_coord)**2 + (current_node.y_coord-goal_node.y_coord)**2)
    
    current_f = new_g + new_h
    return new_g, new_h, current_f

#initializing values required for the A* search
priority_queue = PriorityQueue()
nodes_explored = 0
start = timer()
start_node, end_node = create_graph(maze_matrix)
start_node.g = 0
start_node.h = 0
start_node.f = 0
A_star_search(start_node, end_node)

path = []
current_node = end_node
while current_node != start_node:
    path = [current_node] + path
    current_node = current_node.previous_node
path = [start_node] + path

end = timer()

#To show path highlighted in green and visited nodes in red
for node in maze_graph.nodes.values():
    if node.is_visited():
        display_matrix[node.x_coord][node.y_coord] = "\033[1;91m-\033[0m"
display_matrix[path[0].x_coord][path[0].y_coord] = "\033[1;32mS\033[0m"
for node in path[1:-1]:
    display_matrix[node.x_coord][node.y_coord] = "\033[1;32mP\033[0m"
display_matrix[path[-1].x_coord][path[-1].y_coord] = "\033[1;32mE\033[0m"

display_maze(display_matrix)
print("\n==========================\n")
#Displaying the path
for node in path[:-1]:
    print("Node(%d, %d)" %(node.x_coord, node.y_coord), end='->')
print("Node(%d, %d)" %(path[-1].x_coord, path[-1].y_coord))
print("\n==========================\n")
print("Nodes explored: %d " %nodes_explored)
print("Time of execution: %f" %(end-start))
print("Path length: %d" %len(path))