import dataclasses as dc
import typing
from datetime import datetime

import sqlalchemy as sa

from base_module.base_models import BaseOrmMappedModel, ValuedEnum

SCHEMA_NAME = 'image_tasks'

class TaskStatus(ValuedEnum):
    """."""
    NEW = "new"
    PROCESSING = "processing"
    ERROR = "error"
    DONE = "done"

    def __json__(self):
        return self.value

@dc.dataclass
class ProcessingTask(BaseOrmMappedModel):
    """."""

    __tablename__ = "image_tasks"
    __table_args__ = {'schema': SCHEMA_NAME}

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
    process_status: TaskStatus = dc.field(
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
        metadata={"sa": sa.Column(sa.JSON, nullable=False)}
    )
    process_time: int = dc.field(
        default=0,
        metadata={"sa": sa.Column(sa.Integer(), nullable=False)}
    )

BaseOrmMappedModel.REGISTRY.mapped(ProcessingTask)
