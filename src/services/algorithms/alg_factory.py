from base_module.base_models import (
    ModuleException,
    ClassesLoggerAdapter
)
from .projection import ProjectionAlgorithm
from .resolution import ResolutionAlgorithm


class AlgorithmFactory:
    def __init__(self):
        self._logger = ClassesLoggerAdapter.create(self)

    _registry = {
        "projection": ProjectionAlgorithm,
        "resolution": ResolutionAlgorithm,
    }
    _save_path = {
        "projection": "projection",
        "resolution": "resolution",
    }

    @classmethod
    def get_algorithm(cls, name: str):
        if name not in cls._registry:
            raise ModuleException('Неизвестный алгоритм', code=400)
        return cls._registry[name]()

    @classmethod
    def get_save_path(cls, path: str):
        return cls._save_path[path]
