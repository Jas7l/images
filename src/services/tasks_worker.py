import os.path
import shutil
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Session as PGSession

from base_module.base_models import BaseMule, ClassesLoggerAdapter
from base_module.base_models import ModuleException
from base_module.models import TaskIdentMessageModel

from base_module.services import RabbitService

from models.orm_models import ProcessingTask, TaskStatus


class TasksWorker(BaseMule):
    """Сервис обработки задач"""

    def __init__(
            self,
            rabbit: RabbitService,
            pg_connection: PGSession,
            temp_dir: str,
            storage_dir: str,
    ):
        """Инициализация сервиса"""
        self._rabbit = rabbit
        self._pg = pg_connection
        self._temp_dir = temp_dir
        self._storage_dir = storage_dir
        self._logger = ClassesLoggerAdapter.create(self)

    def _work_dir(self, task_id: int) -> str:
        """Создание временной папки"""
        temp_dir = os.path.join(self._temp_dir, str(task_id))
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir



    def _handle(self, task: ProcessingTask):
        """Обработка задачи"""
        self._logger.info('Обработка задачи', extra={'task': task.task_id})
        task = ProcessingTask.load(task.dump())

        with self._pg.begin():
            temp_dir = self._work_dir(task.task_id)
            try:

                self._update_status(task, TaskStatus.DONE)
            except Exception as e:
                self._logger.critical(
                    'Ошибка обработки задачи',
                    exc_info=True,
                    extra={'e': e, 'task': task.task_id}
                )
                self._update_status(task, TaskStatus.ERROR)
            finally:
                shutil.rmtree(temp_dir, ignore_errors=True)
                self._logger.info(
                    'Обработка задачи завершена',
                    extra={'task': task.task_id}
                )

    def _update_status(self, task: ProcessingTask, status: TaskStatus):
        """Обновление статуса задачи"""
        task.status = status
        updated = datetime.now()
        task.duration = (updated - task.updated_at).total_seconds()
        task.updated_at = updated
        self._logger.info(
            'Изменение статуса задачи',
            extra={'task_id': task.task_id, 'status': task.status}
        )
        with self._pg.begin():
            if self._pg.get(ProcessingTask, task.task_id,
                            with_for_update=True):
                self._pg.merge(task)
                return task.reload()

    def _get_task(self, task_id: int) -> ProcessingTask | None:
        """Получение задачи из БД"""
        with self._pg.begin():
            task: ProcessingTask = self._pg.execute(
                sa.select(ProcessingTask).filter(
                    sa.and_(
                        sa_operator.eq(ProcessingTask.task_id, task_id),
                        sa_operator.in_(
                            ProcessingTask.status,
                            [
                                TaskStatus.NEW,
                                # В случае ручного восстановления работы
                                TaskStatus.PROCESSING
                            ]
                        )
                    )
                ).limit(1)
            ).scalar()
            if not task:
                return

            task.status = TaskStatus.PROCESSING
            task.updated_at = datetime.now()
            self._pg.merge(task)
            return task.reload()

    def _handle_message(self, message: TaskIdentMessageModel, **_):
        """Обработка сообщения от брокера"""
        task_id = message.payload.task_id
        task = self._get_task(task_id)
        if not task:
            self._logger.warn('Задача не найдена', extra={'task_id': task_id})
            return

        try:
            self._handle(task)
        except Exception as e:
            exc_data = {'e': e}
            if isinstance(e, ModuleException):
                exc_data.update(e.data)
            self._logger.critical(
                'Ошибка верхнего уровня обработчика задачи',
                extra=exc_data, exc_info=True
            )
            self._update_status(task, TaskStatus.ERROR)

    def run(self):
        """Запуск прослушивания очереди брокера сообщений"""
        self._rabbit.run_consume(self._handle_message, TaskIdentMessageModel)
