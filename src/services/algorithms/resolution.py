import os

from osgeo import gdal

from base_module.base_models import ModuleException
from .base import BaseAlgorithm


class ResolutionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str,
            algorithm_params: dict,
            input_file_path: str):
        input_dir = os.path.dirname(input_file_path)
        new_name = algorithm_params.get("new_name", "Resolution.tif")
        output_file_path = os.path.join(input_dir, new_name)
        save_path = algorithm_params.get("save_path")

        yres = algorithm_params.get("yRes")
        xres = algorithm_params.get("xRes")
        if not yres or not xres:
            raise ModuleException("Обязательные параметры: 'yRes', 'xRes'",
                                  code=400)

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
