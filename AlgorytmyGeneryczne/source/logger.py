import typing

import source.observation as observation
import source.environment as environment
import source.population as pop


class Logger(observation.Observer):
    def update(self, subject) -> None:
        if isinstance(subject, environment.Environment):
            self._algorithm_logger(subject)
             
    def _algorithm_logger(self, subject: environment.Environment):
        pass


class VerboseLogger(Logger):
    _iteration_template = "Iteration: {current_iteration:3d}/{all_iterations:<3d} | Best scores: {best_specimens}"
    _best_specimen_template = "Best specimen - score: {score:5d} | genes: {genes}"
    
    def __init__(self, log_frequency: int, number_of_specimens: int = 5) -> None:
        self.log_frequency = log_frequency
        self.number_of_specimens = number_of_specimens
        self.best_specimen_ever = None
             
    def _algorithm_logger(self, subject: environment.Environment):
        best_specimens = self._get_best_specimens(subject.population)
        self._save_best_specimen(best_specimens)
        
        if subject.finished:
            print(
                self._best_specimen_template.format(
                    score=self.best_specimen_ever[0],
                    genes=self.best_specimen_ever[1]
                )
            )
        elif self._show_statistics(subject):
            print(
                self._iteration_template.format(
                    current_iteration=subject.current_iteration,
                    all_iterations=subject.iterations,
                    best_specimens=[specimen[0] for specimen in  best_specimens],
                )
            )
        
    def _show_statistics(self, subject: environment.Environment) -> bool:
        return subject.current_iteration == subject.iterations or \
            subject.current_iteration % self.log_frequency == 0
        
    def _save_best_specimen(self, best_specimens: typing.List[typing.Tuple[int, typing.List[int]]]) -> None:
        current_best_specimen = best_specimens[0]
        if not self.best_specimen_ever:
            self.best_specimen_ever = current_best_specimen
        else:
            if self.best_specimen_ever[0] > current_best_specimen[0]:
                self.best_specimen_ever = current_best_specimen
    
    def _get_best_specimens(self, population: pop.Population) -> typing.List[typing.Tuple[int, typing.List[int]]]:
        scores = [(specimen.score, specimen.grid) for specimen in population]
        scores.sort(key=lambda s: s[0])
        return scores[:self.number_of_specimens]
    

class SimpleLogger(Logger):
    _iteration_template = "Iteration: {current_iteration:3d}/{all_iterations:<3d}"
          
    def _algorithm_logger(self, subject: environment.Environment):
        print(
            self._iteration_template.format(
                current_iteration=subject.current_iteration,
                all_iterations=subject.iterations
            ),
            end="\r"
        )