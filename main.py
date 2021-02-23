from sys import argv

maze = open(argv[1], "r") 

# Split maze into rows
maze_array = maze.read().split("\n")

maze.close()

class Node:
    def __init__(self, x_coord, y_coord, parent=None, heuristic=None):
        self.x = x_coord 
        self.y = y_coord
        self.parent = parent
        self.heuristic = heuristic

    def neighbouring_nodes(self, maze_array):
        poss_neighbours = []

        poss_neighbours.append((self.x, self.y + 1))  # Down neighbour
        poss_neighbours.append((self.x, self.y - 1))  # Up neighbour
        poss_neighbours.append((self.x + 1, self.y))  # Right neighbour
        poss_neighbours.append((self.x - 1, self.y))  # Left neighbour

        act_neighbours = []
        for neighbour in poss_neighbours:
            if 0 <= neighbour[1] < len(maze_array): # If neighbour's y coordinate is between 0 and the number of rows
                if 0 <= neighbour[0] < len(maze_array[neighbour[1]]): # If the neighbour's x coordinate is between 0 and the number of columns
                    if maze_array[neighbour[1]][neighbour[0]] != "#": # If the neighbour is not a wall
                        act_neighbours.append(neighbour)

        return act_neighbours
    
    def equals(node1, node2):
        return node1.x == node2.x and node1.y == node2.y
    
    def manhattan_heuristic(self, end_pos):
        self.heuristic = abs(self.x - end_pos.x) + abs(self.y - end_pos.y)

    def __repr__(self):
        return f"{self.x} {self.y} {self.heuristic}"
class Solve:
    def __init__(self, maze_array, depth=False, breadth=False, greedy=False):
        self.array = maze_array
        self.depth = depth
        self.breadth = breadth
        self.greedy = greedy

        self.explored = []
        self.frontier = []
        self.end_pos = None

    def find_end_pos(self):
        for i in range(len(self.array)):
            for j in range(len(self.array[i])):
                if self.array[i][j] == "B":
                    self.end_pos = Node(j, i)
                    return None

    def check_node_not_in(self, set_of_nodes, node_to_check):
        for node in set_of_nodes:
            if node_to_check.equals(node):
                return False
        return True

    def add_neighbours_to_frontier(self, current_node):
        neighbours = current_node.neighbouring_nodes(self.array)

        for neighbour in neighbours:
            node_neighbour = Node(neighbour[0], neighbour[1], current_node)
            if self.check_node_not_in(self.explored, node_neighbour):
                if self.greedy:
                    node_neighbour.manhattan_heuristic(self.end_pos)
                self.frontier.append(node_neighbour)

    def goal_test(self, current_node):
        if maze_array[current_node.y][current_node.x] == "B": # Check to see if the current node is the goasl
            print("Solution Found.")
            solution = [(current_node.x, current_node.y)]
            while current_node.parent: 
                solution.append((current_node.parent.x, current_node.parent.y))
                current_node = current_node.parent

            explored_squares = []
            for square in self.explored:
                explored_squares.append((square.x, square.y))
            return [solution, explored_squares]

        return None

    def solve_maze(self):
        start_pos = Node(maze_array[0].index("A"), 0)
        self.start_pos = start_pos
        
        if self.greedy:
            self.find_end_pos()  

        self.frontier.append(start_pos)

        while True:
            if self.frontier == []:
                print("No Solution.")
                return 0
            if self.breadth:
                current_node = self.frontier[0]
                self.frontier = self.frontier[1:]
            elif self.depth:
                current_node = self.frontier[-1]
                self.frontier = self.frontier[:-1]  
            else:
                self.frontier.sort(key=lambda node: node.heuristic)
                current_node = self.frontier[0]
                self.frontier = self.frontier[1:]

            test_for_goal = self.goal_test(current_node)

            if test_for_goal:
                return test_for_goal

            self.add_neighbours_to_frontier(current_node)
            self.explored.append(current_node)


def draw_solution(solution, maze_array, show_explored=False):
    solution_string = ""

    try:
        solved = solution[0]
        explored = solution[1]
    except:
        return None

    for i in range(len(maze_array)):
        for j in range(len(maze_array[i])):
            if (j, i) in solved:
                if maze_array[i][j] in ("A", "B"):
                    solution_string += f"\u001b[32m{maze_array[i][j]}\u001b[0m"
                else:
                    solution_string += f"\u001b[31mx\u001b[0m"
            elif show_explored and (j, i) in explored:
                solution_string += f"\u001b[33mx\u001b[0m"
            else:
                solution_string += maze_array[i][j]

        solution_string += "\n"
    print(solution_string)


print("Breadth First Search:")
draw_solution(Solve(maze_array, breadth=True).solve_maze(), maze_array)

print("Depth First Search")
draw_solution(Solve(maze_array, depth=True).solve_maze(), maze_array)

print("Greedy Search with a Manhattan Distance Heuristic:")
draw_solution(Solve(maze_array, greedy=True).solve_maze(), maze_array)


