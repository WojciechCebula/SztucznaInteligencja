import typing
import random

import grid


class Selector:
    def select(self, population: typing.List[grid.Grid]) -> typing.List[grid.Grid]:
        pass
    
    def _calculate_fitness_sum(self, population: typing.List[grid.Grid]) -> float:
        return sum(sub.fitness for sub in population)


class RouletteSelector(Selector):
    def select(self, population: typing.List[grid.Grid]) -> typing.List[grid.Grid]:
        new_population = []
        accumulated_probabilities = self._create_accumulated_probabilities(population)
        
        for _ in population:
            new_population.append(self._single_roulette_wheel(population, accumulated_probabilities))
        
        return new_population
    
    def _single_roulette_wheel(self, population: typing.List[grid.Grid], accumulated_probabilities: typing.List[float]) -> grid.Grid:
        probability = random.random()
        
        for specimen, chance in zip(population, accumulated_probabilities):
            if chance >= probability:
                return grid.Grid.copy(specimen)
        
    def _create_accumulated_probabilities(self, population: typing.List[grid.Grid]) -> typing.List[float]:
        accumulated_probabilities = []
        fitness_sum = self._calculate_fitness_sum(population)
        probability_sum = 0
        
        for specimen in population:
            probability_sum += specimen.fitness / fitness_sum
            accumulated_probabilities.append(probability_sum)
        
        if len(accumulated_probabilities):
            accumulated_probabilities[-1] = 1
        
        return accumulated_probabilities

class TournamentSelector(Selector):
    def __init__(self, tournament_batch_size: int) -> None:
        super().__init__()
        self.tournament_batch_size = tournament_batch_size
    
    def select(self, population: typing.List[grid.Grid]) -> typing.List[grid.Grid]:
        new_population = []
        
        for _ in population:
            competitors = random.sample(population, self.tournament_batch_size)
            new_population.append(grid.Grid.copy(self._select_winner(competitors)))
        
        return new_population
    
    def _select_winner(self, competitors: typing.List[grid.Grid]) -> grid.Grid:
        winner = competitors[0]
        
        for competitor in competitors:
            if competitor.fitness > winner.fitness:
                winner = competitor
        
        return winner
        