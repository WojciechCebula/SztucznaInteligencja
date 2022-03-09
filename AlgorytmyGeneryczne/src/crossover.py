import random
import typing

import grid


class Crossover:
    def __init__(self, probability: float) -> None:
        self.probability = probability
    
    def crossover(self, population: typing.List[grid.Grid]) -> None:
        pass


class SinglePointCrossover(Crossover):
    def crossover(self, population: typing.List[grid.Grid]) -> None:
        size = len(population)
        if size % 2 == 1:
            size -= 1

        for i in range(0, size, 2):
            if self.probability > random.random():
                self._crossover_one(population[i], population[i + 1])
    
    def _crossover_one(self, first: grid.Grid, second: grid.Grid) -> None:
        size = first.mode.occupancy
        cut_point = random.randint(0, size)
        
        used = {}
        used_reversed = {}
        
        for i in range(cut_point):
            old = first.grid[i]
            new = second.grid[i]
            
            if old != new:
                if new not in used_reversed and old not in used:
                    used[new] = old
                    used_reversed[old] = new
                elif new in used_reversed and old in used:
                    used[used_reversed[new]] = used[old]
                    used_reversed[used[old]] = used_reversed[new]
                    used.pop(old)
                    used_reversed.pop(new)
                elif new in used_reversed:
                    used_reversed[old] = used_reversed[new]
                    used[used_reversed[new]] = old
                    used_reversed.pop(new)
                else:
                    used[new] = used[old]
                    used_reversed[used[new]] = new
                    used.pop(old)

                first.grid[i] = new
                second.grid[i] = old
        
        for i in range(cut_point, size):
            first_gen = first.grid[i] 
            if first_gen in used:
                first.grid[i] = used[first_gen]
            
            second_gen = second.grid[i] 
            if second_gen in used_reversed:
                second.grid[i] = used_reversed[second_gen]
 