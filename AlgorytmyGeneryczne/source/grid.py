import random

import source.modes as modes


class Grid:
    def __init__(self, mode: modes.Mode, grid: list = []) -> None:
        self.mode = mode
        self.grid = grid
        self.score = None
        self.fitness = None
     
    def calculate_score(self):
        result = 0
        for source, destinations in self.mode.connections.items():
            for dest in destinations:
                result += self._calculate_score_for_one(source, dest)
        self.score = result
        self.fitness = 1 / result
        return result
    
    def _calculate_score_for_one(self, source: int, dest: int):
        distance = self._count_distance(source, dest)
        cost = self.mode.get_cost(source, dest)
        flow = self.mode.get_flow(source, dest)
        return distance * cost * flow
    
    def _count_distance(self, source: int, dest: int):
        source_position = self.grid[source]
        dest_position = self.grid[dest]
        height = self.mode.height
        width = self.mode.width
        return abs(source_position % width - dest_position % width) + \
                abs(source_position // width - dest_position // width)
    
    def _randomize_grid(self) -> None:
        size = self.mode.width * self.mode.height
        machines = list(range(size))
        random.shuffle(machines)
        machines = machines[0:self.mode.occupancy]
        self.grid = machines

    @classmethod
    def copy(cls, other):
        new = cls(other.mode, list(other.grid))
        new.score = other.score
        new.fitness = other.fitness
        return new

    @classmethod
    def create_randomized_instance(cls, mode: modes.Mode):
        obj = cls(mode)
        obj._randomize_grid()
        obj.calculate_score()
        return obj
    
    def __gt__(self, other):
        return self.score > other.score
    