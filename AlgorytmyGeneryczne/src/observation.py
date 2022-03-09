import typing
import abc


class Observer:
    @abc.abstractmethod
    def update(self, subject) -> None:
        pass


class Observable:
    _observers: typing.List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self)