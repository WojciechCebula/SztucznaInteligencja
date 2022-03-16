import pickle
import typing
import os

import matplotlib.pyplot as plt


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


def plot_diagrams(best_history, average_history, worst_history, label):
    fig = plt.figure()
    fig.tight_layout()
    ax = fig.add_subplot()
    ax.set_title(label)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Score")
    
    ymax = worst_history[0]
    xmax = len(worst_history)
    
    ax.plot(worst_history, color="r", label="worst")
    ax.plot(average_history, color="y", label="average")
    ax.plot(best_history, color="g", label="best")
    
    add_annotation(ax, worst_history, ymax, xmax)
    add_annotation(ax, average_history, ymax, xmax)
    add_annotation(ax, best_history, ymax, xmax)
    ax.legend(bbox_to_anchor=(1.3, 1))

    plt.show()


def add_annotation(ax, history: list, ymax, xmax):
    reversed_history = list(history)
    reversed_history.reverse()
    xcoord = len(reversed_history) - reversed_history.index(min(reversed_history)) - 1
    ycoord = min(reversed_history)
    xtextcoord = xcoord - xmax // 5
    ytextcoord = ycoord + ymax // 15
    
    ax.annotate(
        ycoord, xy=(xcoord, ycoord), xycoords='data',
        xytext=(xtextcoord, ytextcoord), textcoords='data',
        arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=135")
    )


def plot_histogram(data: typing.List[float], title: str) -> None:
    plt.hist(data, bins=100, density=True, histtype="stepfilled")
    plt.ylabel('Probability')
    plt.xlabel('Data')
    plt.title(title)
    plt.show()
