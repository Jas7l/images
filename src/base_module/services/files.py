import json
import os.path

import requests

from base_module.base_models import ClassesLoggerAdapter
from models.orm_models import ProcessingTask


class FilesService:
    """Сервис отправки запросов модуля files"""

    def __init__(
            self
    ):
        """Инициализация сервиса"""
        self.url = "http://files:8000/api/file"
        self._logger = ClassesLoggerAdapter.create(self)

    def get_file(self, file_id: int):
        file = requests.get(self.url + '/' + str(file_id)).json()
        if not file:
            self._logger.critical("Не удалось получить информацию о файле",
                                  extra={"id": "file_id"})
        return file

    def download_file(self, temp_dir: str, task: ProcessingTask):
        file = self.get_file(task.input_file_id)
        file_path = os.path.join(temp_dir,
                                 f"{file['name']}."
                                 f"{file['extension']}")

        try:
            with requests.get(f"{self.url}/{task.input_file_id}/download",
                              stream=True) as r, open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)

            return file_path

        except Exception as e:
            self._logger.critical("Не удалось загрузить файл",
                                  extra={"e": e, "file": file.id})

    def send_file(self, local_path: str, save_path: str):
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
                self.url, files=files, data=data
            )

            response.raise_for_status()
            return response.json()
