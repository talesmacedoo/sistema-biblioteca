from abc import ABC, abstractmethod

class Command(ABC):
    """interface command"""
    @abstractmethod
    def execute(self):
        pass