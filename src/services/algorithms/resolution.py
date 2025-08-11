import os

from osgeo import gdal

from .base import BaseAlgorithm


class ResolutionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str, algorithm_params: dict, input_file_path: str):
        input_dir = os.path.dirname(input_file_path)
        new_name = algorithm_params.get("new_name", "Resolution.tif")
        output_file_path = os.path.join(input_dir, new_name)
        save_path = algorithm_params.get("save_path")

        gdal.Warp(
            output_file_path,
            input_file_path,
            options=gdal.WarpOptions(
                xRes=algorithm_params.get('xRes'),
                yRes=algorithm_params.get('yRes')
            )
        )

        res = self.send_file(output_file_path, save_path)

        return res