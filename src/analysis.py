class Analysis:

    def __init__(self):
        self.gen_count = 0
        self.data_dictionary = {}

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
