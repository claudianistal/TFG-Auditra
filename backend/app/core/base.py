from abc import ABC, abstractmethod

class AudioStrategy(ABC):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    @abstractmethod
    def run(self, file_path: str) -> dict:
        """Cada estrategia debe implementar este método"""
        pass