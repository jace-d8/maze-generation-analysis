from app import App
import math


class Analysis:
    """
    The total count here is meant to count the total amount of turns taken (which can vary depending on the maze
    size) to calculate the percentage in which a direction is chosen. When init is called it will open the data file and
    populate the dictionary with the encapsulated data.
    """

    def __init__(self):
        self.total_count = 0
        self.current_count = 0
        self.total_direction_count = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.current_direction_count = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.matrix = []
        self.probability_distribution = []
        self.entropy = 0
        self.load()

    def load(self):
        with open("../data/data.txt", 'r') as data:
            temp = 0
            data.readline()  # Skip the first line of file
            for line in data:
                temp += 1
                direction, other = line.strip().split(': ')
                count = other.split(' - ')[0]  # the [0] is select the first element in the list as the split
                # generates two, the number before the dash and the number after
                self.total_direction_count[direction] = int(count)
                if temp == 4:
                    break

    # P(E) should be 1/4 as S = 4 and E = 1
    def directional_variation(self, direction):
        if direction in self.total_direction_count:
            self.total_direction_count[direction] += 1
            self.current_direction_count[direction] += 1
            self.current_count += 1

    def update_data(self):
        self.total_count = sum(self.total_direction_count.values())
        with open("../data/data.txt", 'w') as data:
            data.write("Total direction counter: count - percentage\n")

            for direction, count in self.total_direction_count.items():
                if self.total_count != 0:
                    percentage = count / self.total_count
                    data.write(f"{direction}: {count} - {percentage * 100:.3f}%\n")
            data.write("Current direction counter: count - percentage\n")

            for direction, count in self.current_direction_count.items():
                if self.current_count != 0:
                    percentage = count / self.current_count
                    data.write(f"{direction}: {count} - {percentage * 100:.3f}%\n")
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
            # OPTIMIZE

    # Shannon's entropy details in readme, 2^x = 14 (possible outcomes) where x = perfect entropy
    def shannons_entropy(self):
        self.entropy = -sum(p * math.log2(p) for p in self.probability_distribution if p > 0)

    def run(self, maze):
        self.update_data()
        self.convert_maze(maze)
        self.calculate_probability_distribution()
        self.shannons_entropy()
