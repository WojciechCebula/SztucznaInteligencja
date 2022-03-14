import source.observation as observation
import source.mutation as mutation
import source.crossover as cross
import source.population as pop
import source.elitism as elite
import source.selector as sel
import source.modes as modes


class Environment(observation.Observable):
    def __init__(
        self,
        mode: modes.Mode, 
        selector: sel.Selector, 
        mutator: mutation.Mutator, 
        crossover: cross.Crossover,
        elitism: elite.Elitism,
        logger: observation.Observer = None,
        collector: observation.Observer = None
        
    ) -> None:
        self.selector = selector
        self.mode = mode
        self.population = pop.Population(self.mode)
        self.mutator = mutator
        self.crossover = crossover
        self.elitism = elitism
        self.iterations = 0
        self.current_iteration = 0
        self.initialized = False
        self.finished = False
        if logger:
            self.attach(logger)
        if collector:
            self.attach(collector)
    
    def init(self, size: int):
        self.population.create_initial_population(size)
        self.initialized = True
    
    def reset(self, size: int):
        self.iterations = 0
        self.current_iteration = 0
        self.finished = False
        self.population.create_initial_population(size)
        
    def run(self, iterations: int) -> None:
        if not self.initialized:
            raise ValueError("Initialize object with 'init' function.")
        self.iterations = iterations
        
        self._notify()
        
        for iteration in range(self.iterations):
            self.current_iteration = iteration + 1
            try:
                self._iterate()
                self._notify()
            except KeyboardInterrupt:
                break
        self.finished = True
        self._notify()

    def _iterate(self) -> None:
        self.elitism.sample_elite(self.population)
        
        new_population = self.selector.select(self.population.specimens)
        
        self.crossover.crossover(new_population)
        
        self.mutator.mutate(new_population)
        
        self.population.specimens = new_population
        
        self.population.calculate_scores()
        
        self.elitism.marge_elite(self.population)
