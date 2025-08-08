import json
import os
from abc import ABC, abstractmethod

import requests


class BaseAlgorithm(ABC):
    @staticmethod
    def send_file(local_path: str, save_path: str):
        filename = os.path.basename(local_path)
        fields = {
            "path": save_path,
        }

        with open(local_path, 'rb') as f:
            files = {
                "attachment": (filename, f, "application/octet-stream")
            }
            data = {
                "fields": json.dumps(fields),
            }
            response = requests.post(
            f"http://files/api/file", files=files, data=data
            )

            response.raise_for_status()
            return response.json()

    @abstractmethod
    def run(self, algorithm: str, algorithm_params: dict, input_file_path: str):
        pass