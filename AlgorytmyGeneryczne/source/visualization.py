import pickle
import typing
import os


def load_results(dir_path: str) -> dict:
    results = {}
    for file_name in os.listdir(dir_path):
        path = os.path.join(dir_path, file_name)
        with open(path, "rb") as file:
            data = pickle.load(file)
            results[file_name.rstrip(".pkl")] = data
    return results

def gather_all_statistics(iterations: typing.List[typing.List[typing.Tuple[typing.List[int], int]]]) -> typing.Tuple[typing.List[int], typing.List[int], typing.List[int]]:
    best_history = []
    average_history = []
    worst_history = []
    for population in iterations:
        best, average, worst = get_population_statistics(population)
        best_history.append(best)
        average_history.append(average)
        worst_history.append(worst)
    
    return best_history, average_history, worst_history


def get_population_statistics(population: typing.List[typing.Tuple[typing.List[int], int]]) -> typing.Tuple[int, int, int]:
    only_scores = sorted(specimen[1] for specimen in population)
    return only_scores[0], sum(only_scores) // len(only_scores), only_scores[-1]


def add_annotation(ax, history, ymax, xmax):
    xcoord = len(history) - 1
    ycoord = history[-1]
    xtextcoord = xcoord - xmax // 5
    ytextcoord = ycoord + ymax // 15
    
    ax.annotate(
        ycoord, xy=(xcoord, ycoord), xycoords='data',
        xytext=(xtextcoord, ytextcoord), textcoords='data',
        arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=135")
    )