import dataclasses as dc

from osgeo import gdal

from base_module.base_models import ModuleException, Model
from .base import BaseAlgorithm


@dc.dataclass
class AlgorithmParams(Model):
    yres: float = dc.field()
    xres: float = dc.field()


class ResolutionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str,
            algorithm_params: dict,
            input_file_path: str):
        resolution_params = AlgorithmParams(
            yres=algorithm_params.get("yRes"),
            xres=algorithm_params.get("xRes"),
        )
        yres = resolution_params.yres
        xres = resolution_params.xres
        if not yres or not xres:
            raise ModuleException(
                "Обязательные параметры: 'yRes', 'xRes'",
                code=400
            )

        output_file_path = self.generate_output_path(input_file_path)
        save_path = "resolution"

        gdal.Warp(
            output_file_path,
            input_file_path,
            options=gdal.WarpOptions(
                xRes=xres,
                yRes=yres
            )
        )

        res = {"output_file_path": output_file_path, "save_path": save_path}
        return res
