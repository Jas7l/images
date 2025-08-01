import dataclasses as dc
import enum
import typing
from datetime import datetime

import sqlalchemy as sa

from base_module.base_models import BaseOrmMappedModel

SCHEMA_NAME = 'external_module'

class TaskStatus(enum.Enum):
    """."""
    NEW = "new"
    PROCESSING = "processing"
    ERROR = "error"
    DONE = "done"

@dc.dataclass
class ProcessingTask(BaseOrmMappedModel):
    """."""

    __tablename__ = "image_tasks"

    task_id: int = dc.field(
        default=None,
        metadata={"sa": sa.Column(
            sa.Integer, autoincrement=True, primary_key=True
        )}
    )
    created_date: datetime = dc.field(
        default_factory=datetime.utcnow,
        metadata={"sa": sa.Column(sa.DateTime())}
    )
    updated_date: typing.Optional[datetime] = dc.field(
        default_factory=datetime.utcnow,
        metadata={"sa": sa.Column(
            sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()
        )}
    )
    process_status: str = dc.field(
        default=TaskStatus.NEW,
        metadata={
            'sa': sa.Column(
                sa.Enum(TaskStatus, name="image_task",
                        schema=SCHEMA_NAME)
            )
        }
    )
    input_file_id: int = dc.field(
        default=None,
        metadata={"sa": sa.Column(sa.Integer(), nullable=False)}
    )
    output_file_id: int = dc.field(
        default=None,
        metadata={"sa": sa.Column(sa.Integer(), nullable=True)}
    )
    algorithm: str = dc.field(
        default=None,
        metadata={"sa": sa.Column(sa.String(), nullable=False)}
    )
    algorithm_params: dict = dc.field(
        default=None,
        metadata={"sa": sa.Column(sa.DictType(), nullable=False)}
    )
    process_time: int = dc.field(
        default=0,
        metadata={"sa": sa.Column(sa.Integer(), nullable=False)}
    )

BaseOrmMappedModel.REGISTRY.mapped(ProcessingTask)
