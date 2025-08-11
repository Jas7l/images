import os

from osgeo import gdal

from .base import BaseAlgorithm


class ProjectionAlgorithm(BaseAlgorithm):
    def run(self, algorithm: str, algorithm_params: dict, input_file_path: str):
        input_dir = os.path.dirname(input_file_path)
        new_name = algorithm_params.get("new_name", "Reprojection.tif")
        output_file_path = os.path.join(input_dir, new_name)
        save_path = algorithm_params.get("save_path")

        dst_srs = algorithm_params.get("dstSRS")
        if not dst_srs:
            raise ValueError("Обязательные параметры: 'dstSRS'")

        gdal.Warp(
            output_file_path,
            input_file_path,
            dstSRS=dst_srs,
        )

        res = self.send_file(output_file_path, save_path)

        return res