import dataclasses as dc
from typing import Any

import pika
import sqlalchemy as sa
from sqlalchemy.orm import Session as PGSession

from base_module.base_models import Model
from base_module.base_models import (
    ModuleException,
    ClassesLoggerAdapter
)
from base_module.models import TaskIdentMessageModel
from base_module.services import RabbitService
from models import ProcessingTask


@dc.dataclass
class CreationModel(Model):
    """."""

    input_file_id: int = dc.field()
    algorithm: str = dc.field()
    algorithm_params: dict = dc.field()


class TasksService:
    """."""

    def __init__(
            self,
            rabbit: RabbitService,
            pg_connection: PGSession
    ):
        """."""
        self._rabbit = rabbit
        self._pg = pg_connection
        self._logger = ClassesLoggerAdapter.create(self)

    def create_task(self, data) -> dict:
        """."""

        data = CreationModel.load(data)

        task = (
            ProcessingTask(
                input_file_id=data.input_file_id,
                algorithm=data.algorithm,
                algorithm_params=data.algorithm_params,
            )
        )

        with self._pg.begin():
            self._pg.add(task)
            self._pg.flush()
            task_id = task.task_id

        message = TaskIdentMessageModel.lazy_load(
            TaskIdentMessageModel.T(task_id))
        message_dict = message.dump()

        published = self._rabbit.publish(
            message_dict, properties=pika.BasicProperties()
        )
        if published:
            return task.dump()

        raise ModuleException(
            'Не удалось отправить сообщения об обработке задач'
        )

    def get_all(self) -> list[dict[str, Any]]:
        """."""
        with self._pg.begin():
            q = self._pg.query(ProcessingTask)

            q = q.order_by(sa.desc(ProcessingTask.created_date))
            tasks = q.all()
            return [task.dump() for task in tasks]

    def get(self, task_id: int) -> dict[str, Any]:
        with self._pg.begin():
            task: ProcessingTask = self._pg.query(
                ProcessingTask).get(task_id)
            if task:
                return task.dump()

        raise ModuleException('Задача не найдена', code=404)
