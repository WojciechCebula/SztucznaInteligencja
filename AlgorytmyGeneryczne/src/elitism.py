import typing

import population as pop
import grid


class Elitism:
    def __init__(self, probability: float) -> None:
        self.elite = []
        self.probability = probability
    
    def sample_elite(self, population: pop.Population) -> typing.List[grid.Grid]:
        sorted_population = sorted(population.specimens)
        size = int(len(sorted_population) * self.probability)
        self.elite = [grid.Grid.copy(specimen) for specimen in sorted_population[:size]]
        
    def marge_elite(self, population: pop.Population) -> None:
        sorted_population = sorted(population.specimens)
        population.specimens = sorted_population[0:-len(self.elite)] + self.elite
