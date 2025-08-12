import dataclasses as dc

from osgeo import gdal

from base_module.base_models import ModuleException, Model
from .base import BaseAlgorithm


@dc.dataclass
class AlgorithmParams(Model):
    dst_srs: str = dc.field()


class ProjectionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str,
            algorithm_params: dict,
            input_file_path: str):
        projection_pramas = AlgorithmParams(
            dst_srs=algorithm_params.get('dstSRS')
        )
        if not projection_pramas:
            raise ModuleException(
                "Обязательные параметры: 'dstSRS'",
                code=400
            )

        output_file_path = self.generate_output_path(input_file_path)
        save_path = "projection"

        gdal.Warp(
            output_file_path,
            input_file_path,
            dstSRS=projection_pramas.dst_srs,
        )

        res = {"output_file_path": output_file_path, "save_path": save_path}
        return res
