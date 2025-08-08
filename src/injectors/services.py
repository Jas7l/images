from base_module.services import RabbitService

from config import config
from services import TasksService, TasksWorker
from . import connections


def rabbit() -> RabbitService:
    """."""
    return RabbitService(config.rabbit)


def tasks_service() -> TasksService:
    """."""
    return TasksService(
        rabbit=rabbit(),
        pg_connection=connections.pg.acquire_session()
    )


def tasks_mule() -> TasksWorker:
    """."""
    return TasksWorker(
        rabbit=rabbit(),
        pg_connection=connections.pg.acquire_session(),
        temp_dir=config.tmp_dir
    )
