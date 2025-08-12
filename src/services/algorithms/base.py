from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    @abstractmethod
    def run(self, algorithm: str, algorithm_params: dict,
            input_file_path: str):
        pass
