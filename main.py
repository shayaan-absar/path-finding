from sys import argv

maze = open(argv[1], "r")

# Parsing the Maze
maze_array = maze.read().split("\n")

maze.close()

class Node:
    def __init__(self, x_coord, y_coord, parent = None):
        self.x = x_coord
        self.y = y_coord
        self.parent = parent

    def neighbouring_nodes(self, maze_array):
        poss_neighbours = []

        poss_neighbours.append((self.x, self.y + 1))  # Down neighbour
        poss_neighbours.append((self.x, self.y - 1))  # Up neighbour
        poss_neighbours.append((self.x + 1, self.y))  # Right neighbour
        poss_neighbours.append((self.x - 1, self.y))  # Left neighbour

        act_neighbours = []
        for neighbour in poss_neighbours:
            if 0 <= neighbour[1] < len(maze_array):
                if 0 <= neighbour[0] < len(maze_array[neighbour[1]]):
                    if maze_array[neighbour[1]][neighbour[0]] != "#":
                        act_neighbours.append(neighbour)
        return act_neighbours 
    def equals(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"{self.x} {self.y}"

def check_node_not_in(set_of_nodes, node_to_check):
    for node in set_of_nodes:
        if node_to_check.equals(node):
            return False
    return True

def depth_first_search(maze_array, breadth = False):
    frontier = []
    start_pos = Node(maze_array[0].index("A"), 0)
    frontier.append(start_pos)
    explored = []
    while True:
        if frontier == []:
            print("No Solution.")
            exit()
        if breadth:
            current_node = frontier[0]
            frontier = frontier[1:]
        else:
            current_node = frontier[-1]
            frontier = frontier[:-1]
        
        if maze_array[current_node.y][current_node.x] == "B":
            print("Solution Found.")
            solution = [(current_node.x, current_node.y)]
            while current_node.parent: 
                solution.append((current_node.parent.x, current_node.parent.y))
                current_node = current_node.parent
            return solution

        neighbours = current_node.neighbouring_nodes(maze_array)

        for neighbour in neighbours:
            node_neighbour = Node(neighbour[0], neighbour[1], current_node)
            if check_node_not_in(explored, node_neighbour):
                frontier.append(node_neighbour)
        explored.append(current_node)

def draw_solution(solution, maze_array):
    solution_string = ""

    for i in range(len(maze_array)):
        for j in range(len(maze_array[i])):
            if (j, i) in solution:
                if maze_array[i][j] in ("A", "B"):
                    solution_string += f"\u001b[32m{maze_array[i][j]}\u001b[0m"
                else:
                    solution_string += f"\u001b[31mx\u001b[0m"
            else:
                solution_string += maze_array[i][j]

        solution_string += "\n"
    print(solution_string)

print("Breadth First Search:")
draw_solution(depth_first_search(maze_array, True), maze_array)

print("Depth First Search")
draw_solution(depth_first_search(maze_array), maze_array)
