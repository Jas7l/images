import dataclasses as dc
import typing as t

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

    task_id: int = dc.field()
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

    def create_task(self, data) -> ProcessingTask:
        """."""

        data = CreationModel.load(data)

        task = (
            ProcessingTask(
                task_id=data.task_id,
                input_file_id=data.input_file_id,
                algorithm=data.algorithm,
                algorithm_params=data.algorithm_params,
            )
        )

        with self._pg.begin():
            self._pg.add(task)

        task = task.reload()
        message = TaskIdentMessageModel.lazy_load(
                TaskIdentMessageModel.T(task.task_id)
        )

        published = self._rabbit.publish(
            message, properties=pika.BasicProperties()
        )
        if published:
            return task

        raise ModuleException(
            'Не удалось отправить сообщения об обработке задач'
        )

    def get_all(self, map_id: int = None) -> list[ProcessingTask]:
        """."""
        with self._pg.begin():
            q = self._pg.query(ProcessingTask).filter(
                sa_operator.eq(
                    ProcessingTask.project,
                    self._oms.auth.get_request_session().project
                )
            )
            if map_id:
                q = q.filter(sa_operator.eq(ProcessingTask.map_id, map_id))

            q = q.order_by(sa.desc(ProcessingTask.created_at))
            return q.all()

    def get(self, task_id: int) -> ProcessingTask:
        with self._pg.begin():
            task: ProcessingTask = self._pg.query(
                ProcessingTask
            ).filter(
                sa.and_(
                    sa_operator.eq(
                        ProcessingTask.project,
                        self._oms.auth.get_request_session().project
                    ),
                    sa_operator.eq(ProcessingTask.task_id, task_id)
                )
            ).one_or_none()
            if task:
                return task

        raise ModuleException('Задача не найдена', code=404)
