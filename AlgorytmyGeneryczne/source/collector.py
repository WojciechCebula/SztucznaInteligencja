import os.path as path
import datetime
import typing
import pickle
import os

import multiprocessing

import source.observation as observation
import source.environment as environment


class Pickled:
    __slots__ = "grid", "score"
    
    def __init__(self, grid: typing.List[int], score) -> None:
        self.grid = grid
        self.score = score

class Collector(observation.Observer):
    _separator = "_"
    _extension = ".pkl"
    
    def __init__(self, save_path: str, pickled_file_name: str, save_interval: int) -> None:
        self.save_path = save_path
        self.pickled_file_name = pickled_file_name
        self.save_interval = save_interval
        self.queue = []
        self.index = 1
        self.file_index = 0
        self._initialize_storage()

    @property
    def small_file_path(self) -> str:
        return path.join(self.save_path, self.pickled_file_name + self._separator + "{index}" + self._extension)

    @property
    def big_file_path(self) -> str:
        return path.join(self.save_path, self.pickled_file_name + self._separator + self.current_time + self._extension)

    @property
    def current_time(self) -> str:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d_%H-%M-%S")

    def update(self, subject) -> None:
        if isinstance(subject, environment.Environment):
            self._collect_and_save(subject)
             
    def _collect_and_save(self, subject: environment.Environment) -> None:
        if not subject.finished:
            generation = [(list(specimen.grid), specimen.score) for specimen in subject.population.specimens]
            self.queue.append(generation)
        
        if (self.index % self.save_interval == 0 or subject.finished) and self.queue:
            process = multiprocessing.Process(target=self._save_data, args=(self.queue, self.small_file_path, self.file_index))
            process.run()
            self.file_index += len(self.queue)
            self.queue = []
        
        if subject.finished:
            self._save_to_single_file()
        
        self.index += 1

    def _initialize_storage(self):
        if not path.exists(self.save_path):
            os.mkdir(self.save_path)
        elif not path.isdir(self.save_path):
            os.mkdir(self.save_path)
    
    def _save_to_single_file(self):
        result = []
        for i in range(self.file_index):
            current_path = self.small_file_path.format(index=i)
            with open(current_path, "rb") as file:
                array = pickle.load(file)
                result.append(array)
            os.remove(current_path)
        with open(self.big_file_path, 'wb') as file:
                pickle.dump(result, file)
        
    @staticmethod
    def _save_data(queue, file_path: str, index: int):
        size = len(queue)
        for i in range(size):
            current_path =  file_path.format(index=index + i)
            with open(current_path, 'wb') as file:
                pickle.dump(queue[i], file)