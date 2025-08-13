import dataclasses as dc

from osgeo import gdal

from base_module.base_models import ModuleException, Model
from .base import BaseAlgorithm


@dc.dataclass
class AlgorithmParams(Model):
    dstSRS: str = dc.field()


class ProjectionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str,
            algorithm_params: dict,
            input_file_path: str):
        projection_params = AlgorithmParams.load(algorithm_params)
        if not projection_params:
            raise ModuleException(
                "Обязательные параметры: 'dstSRS'",
                code=400
            )

        output_file_path = self.generate_output_path(input_file_path)

        gdal.Warp(
            output_file_path,
            input_file_path,
            dstSRS=projection_params.dstSRS,
        )

        return output_file_path
