import reusable

CROSSING_PROBABILITY = 0.6
MUTATION_PROBABILITY = 0.1
ELITE_PROBABILITY = 0.01

TOURNAMENT_BATCH_SIZE = 5
POPULATION_SIZE = 10000
ITERATIONS = 150

DISPLAYED_SPECIMENS = 10
LOG_FREQUENCY = 5

DATA_DIRECTORY = ".data"
CONNECTIONS_FOLDER = "connections"
RESULTS_FOLDER = "results"
PICKLED_DATA_FILENAME = "flat"
SAVE_INTERVAL = 10

reusable.load_env(__name__)

import os.path as path

CONNECTIONS_DIRECTORY = path.join(DATA_DIRECTORY, CONNECTIONS_FOLDER)
RESULTS_DIRECTORY = path.join(DATA_DIRECTORY, RESULTS_FOLDER)