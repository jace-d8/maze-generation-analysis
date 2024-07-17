class Analysis:

    def __init__(self):
        self.direction_counts = {"up": 0, "right": 0, "down": 0, "left": 0}
        self.gen_count = 0

    # P(E) should be 1/4 as S = 4 and E = 1
    def directional_variation(self, direction):
        if direction in self.direction_counts:
            self.direction_counts[direction] += 1
            self.gen_count += 1

