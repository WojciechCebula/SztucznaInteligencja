import os.path as path


import source.mutation as mutation
import source.selector as selector
import source.environment as env
import source.crossover as cross
import source.collector as col
import source.elitism as elite
import source.config as config
import source.logger as log
import source.modes as modes


easy = modes.Mode(
    3, 3, 9, 
    path.join(config.CONNECTIONS_DIRECTORY, "easy_flow.json"), 
    path.join(config.CONNECTIONS_DIRECTORY, "easy_cost.json")
)
flat = modes.Mode(
    1, 12, 12,
    path.join(config.CONNECTIONS_DIRECTORY, "flat_flow.json"), 
    path.join(config.CONNECTIONS_DIRECTORY, "flat_cost.json")
)
hard = modes.Mode(
    5, 6, 24,
    path.join(config.CONNECTIONS_DIRECTORY, "hard_flow.json"), 
    path.join(config.CONNECTIONS_DIRECTORY, "hard_cost.json")
)

roulette_selector = selector.RouletteSelector()

tournament_selector = selector.TournamentSelector(
    config.TOURNAMENT_BATCH_SIZE
)

mutator = mutation.BinaryBitFlipMutator(
    hard,
    config.MUTATION_PROBABILITY
)

crossover = cross.SinglePointCrossover(
    config.CROSSING_PROBABILITY
)

elitism = elite.Elitism(
    config.ELITE_PROBABILITY
)

simple_logger = log.SimpleLogger()

verbose_logger = log.VerboseLogger(
    config.LOG_FREQUENCY,
    config.DISPLAYED_SPECIMENS
)

collector = col.Collector(
    config.RESULTS_DIRECTORY,
    config.PICKLED_DATA_FILENAME,
    config.SAVE_INTERVAL
)

environment = env.Environment(
    flat,
    roulette_selector,
    mutator,
    crossover,
    elitism,
    simple_logger,
    collector
)

environment.init(config.POPULATION_SIZE)

environment.run(config.ITERATIONS, True)
