"""."""
import dataclasses as dc
import os

import yaml

from base_module.base_models import (
    LoggerConfig,
    Model,
    PgConfig
)
from base_module.models import RabbitFullConfig


@dc.dataclass
class ServiceConfig(Model):
    """."""

    rabbit: RabbitFullConfig = dc.field()
    pg: PgConfig
    tmp_dir: str = dc.field(default='/tmp')
    logging: LoggerConfig = dc.field(default=None)


config: ServiceConfig = ServiceConfig.load(
    yaml.safe_load(open(os.getenv('YAML_PATH', "/config.yaml"))) or {}
)

