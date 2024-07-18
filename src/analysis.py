from app import App
import math


class Analysis:
    """
    The generic counter here is meant to count the total amount of turns taken (which can vary depending on the maze
    size) to calculate the percentage in which a direction is chosen. When init is called it will open the data file and
    populate the dictionary with the encapsulated data.
    """

    def __init__(self):
        self.gen_count = 0
        self.data_dictionary = {}
        self.matrix = []
        self.probability_distribution = []

        with open("../data/data.txt", 'r') as data:
            data.readline()  # Skip the first line of file
            for line in data:
                direction, count = line.strip().split(': ')
                self.data_dictionary[direction] = int(count)

    # P(E) should be 1/4 as S = 4 and E = 1
    def directional_variation(self, direction):
        if direction in self.data_dictionary:
            self.data_dictionary[direction] += 1
            self.gen_count += 1

    def update_data(self):
        with open("../data/data.txt", 'w') as data:
            data.write("Current direction: count - percentage\n")
            for direction, count in self.data_dictionary.items():
                data.write(f"{direction}: {count}\n")

    # MAKE INTO PERCENTAGE HERE

    """
    Converts the maze into another 2d array where the cells are represented by a numerical value depending on their 
    formation. This is so a probability distribution can be laid out. 
    """

    def convert_maze(self, maze):
        self.matrix = [[0 for _ in range(App.COLS)] for _ in range(App.ROWS)]
        for i in range(App.COLS):
            for j in range(App.ROWS):
                current_cell = maze.maze[i][j]
                conversion = {
                    (True, True, True, False): 1,  # left, top, right
                    (True, True, False, True): 2,  # bottom, left, top
                    (True, False, True, True): 3,  # left, bottom, right
                    (False, True, True, True): 4,  # bottom, right, top
                    (True, False, True, False): 5,  # left, right
                    (False, True, False, True): 6,  # top, bottom
                    (True, True, False, False): 7,  # left, top
                    (False, True, True, False): 8,  # top, right
                    (True, False, False, True): 9,  # left, bottom
                    (False, False, True, True): 10,  # bottom, right
                    (False, False, False, True): 11,  # bottom
                    (False, True, False, False): 12,  # top
                    (True, False, False, False): 13,  # left
                    (False, False, True, False): 14  # right
                }
                default_cell = (current_cell.walls["left"], current_cell.walls["top"],
                                current_cell.walls["right"], current_cell.walls["bottom"])
                self.matrix[j][i] = conversion.get(default_cell)

    def calculate_probability_distribution(self):
        total_elements = sum(1 for rows in self.matrix for elements in rows if elements != 0)
        for i in range(1, 15):
            count = 0
            for m in range(App.COLS):
                for n in range(App.ROWS):
                    if self.matrix[n][m] == i:
                        count += 1
            current_probability = count / total_elements
            self.probability_distribution.append(current_probability)

    # Shannon's entropy details in readme
    def shannons_entropy(self):
        entropy = -sum(p * math.log2(p) for p in self.probability_distribution if p > 0)
        print(entropy)

    def run(self, maze):
        self.update_data()
        self.convert_maze(maze)
        self.calculate_probability_distribution()
        self.shannons_entropy()