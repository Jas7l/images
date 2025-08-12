import os
import uuid
from abc import ABC, abstractmethod


class BaseAlgorithm(ABC):
    @staticmethod
    def generate_output_path(input_file_path: str) -> str:
        directory = os.path.dirname(input_file_path)
        old_filename = os.path.basename(input_file_path)
        name, ext = os.path.splitext(old_filename)
        random_part = uuid.uuid4().hex[:8]
        new_filename = f"{name}_{random_part}{ext}"
        return os.path.join(directory, new_filename)

    @abstractmethod
    def run(self, algorithm: str, algorithm_params: dict,
            input_file_path: str):
        pass
