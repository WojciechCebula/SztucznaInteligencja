import random
import typing

import source.modes as modes
import source.grid as grid


class Mutator:
    def __init__(self, mode: modes.Mode, probability: float) -> None:
        self.mode = mode
        self.probability = probability
    
    def mutate(self, population: typing.List[grid.Grid]) -> None:
        pass


class BinaryBitFlipMutator(Mutator):
    def mutate(self, population: typing.List[grid.Grid]) -> None:
        for specimen in population:
            self._mutate_one(specimen)
    
    def _mutate_one(self, specimen: grid.Grid) -> None:
        for gene in range(len(specimen.grid)):
            if self.probability > random.random():
                self._gene_mutation(specimen, gene)
    
    def _gene_mutation(self, specimen: grid.Grid, gene: int) -> None:
        new = random.randrange(0, self.mode.width * self.mode.height)
        try:
            index = specimen.grid.index(new)
            specimen.grid[gene], specimen.grid[index] = new, specimen.grid[gene]
        except ValueError:
            specimen.grid[gene] = new