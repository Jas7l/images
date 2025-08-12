from base_module.services import RabbitService, FilesService

from config import config
from services import TasksService, TasksWorker
from services.algorithms import AlgorithmFactory
from . import connections


def rabbit() -> RabbitService:
    """."""
    return RabbitService(config.rabbit)


def files() -> FilesService:
    """."""
    return FilesService(
        files_url=config.files_url
    )

def algorithm() -> AlgorithmFactory:
    """."""
    return AlgorithmFactory()


def tasks_service() -> TasksService:
    """."""
    return TasksService(
        rabbit=rabbit(),
        pg_connection=connections.pg.acquire_session(),
    )


def tasks_mule() -> TasksWorker:
    """."""
    return TasksWorker(
        rabbit=rabbit(),
        files=files(),
        algorithm=algorithm(),
        pg_connection=connections.pg.acquire_session(),
        temp_dir=config.tmp_dir
    )
