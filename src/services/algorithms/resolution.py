import dataclasses as dc

from osgeo import gdal

from base_module.base_models import ModuleException, Model
from .base import BaseAlgorithm


@dc.dataclass
class AlgorithmParams(Model):
    yRes: float = dc.field()
    xRes: float = dc.field()


class ResolutionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str,
            algorithm_params: dict,
            input_file_path: str):
        resolution_params = AlgorithmParams.load(algorithm_params)
        yRes = resolution_params.yRes
        xRes = resolution_params.xRes
        if not yRes or not xRes:
            raise ModuleException(
                "Обязательные параметры: 'yRes', 'xRes'",
                code=400
            )

        output_file_path = self.generate_output_path(input_file_path)

        gdal.Warp(
            output_file_path,
            input_file_path,
            options=gdal.WarpOptions(
                xRes=xRes,
                yRes=yRes
            )
        )

        return output_file_path
