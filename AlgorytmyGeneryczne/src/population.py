import typing

import modes
import grid


class Population:
    def __init__(self, mode: modes.Mode) -> None:
        self.specimens = []
        self.mode = mode
    
    def create_initial_population(self, size: int) -> None:
        self.specimens = self._create_population(size)
    
    def calculate_scores(self) -> None:
        for specimen in self.specimens:
            specimen.calculate_score()

    def _create_population(self, size: int) -> typing.List[grid.Grid]:
        population = []
        for _ in range(size):
            subject = grid.Grid.create_randomized_instance(self.mode)
            population.append(subject)
        return population

    def __delitem__(self, key) -> None:
        del self.specimens[key]

    def __getitem__(self, key) -> grid.Grid:
        return self.specimens[key]

    def __setitem__(self, key, value) -> None:
        self.specimens[key] = value
    
    def __len__(self) -> int:
        return len(self.specimens)