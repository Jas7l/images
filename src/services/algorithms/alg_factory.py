from .projection import ProjectionAlgorithm
from .resolution import ResolutionAlgorithm
from base_module.base_models import (
    ModuleException,
    ClassesLoggerAdapter
)

class AlgorithmFactory:
    def __init__(self):
        self._logger = ClassesLoggerAdapter.create(self)

    _registry = {
        "projection": ProjectionAlgorithm,
        "resolution": ResolutionAlgorithm,
    }

    @classmethod
    def get(cls, name: str):
        if name not in cls._registry:
            raise ModuleException('Неизвестный алгоритм', code=404)
        return cls._registry[name]()
