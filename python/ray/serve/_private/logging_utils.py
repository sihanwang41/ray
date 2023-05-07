import logging
import os
from typing import Optional
import json

import ray
from ray.serve._private.constants import DEBUG_LOG_ENV_VAR, SERVE_LOGGER_NAME


LOG_FILE_FMT = "{component_name}_{component_id}.log"
MESSAGE_FMT = "%(filename)s:%(lineno)d - %(message)s"
REQUEST_ID_FMT = "%(request_id)s "
ROUTE_FMT = "%(route)s "
APP_NAME_FMT = "%(app_name)s "


class ServeFormatter(logging.Formatter):
    """Serve Logging Formatter

    The formatter will generate the log format on the fly based on the field of record.
    """

    def __init__(self, component_name: str, component_id: str):
        self.component_log_fmt = {
            "levelname": "%(levelname)s",
            "asctime": "%(asctime)s",
            "component_name": component_name,
            "component_id": component_id,
        }

    def format(self, record):
        # generate a format string based on the record field.
        cur_format = self.component_log_fmt
        if "request_id" in record.__dict__:
            cur_format["request_id"] = REQUEST_ID_FMT
        if "route" in record.__dict__:
            cur_format["route"] = ROUTE_FMT
        if "app_name" in record.__dict__:
            cur_format["app_name"] = APP_NAME_FMT

        cur_format["message"] = MESSAGE_FMT

        # create a formatter using the format string
        formatter = logging.Formatter(json.dumps(cur_format))

        # format the log record using the formatter
        return formatter.format(record)


def access_log_msg(*, method: str, status: str, latency_ms: float):
    """Returns a formatted message for an HTTP or ServeHandle access log."""
    return f"{method.upper()} {status.upper()} {latency_ms:.1f}ms"


def log_to_stderr_filter(record: logging.LogRecord) -> bool:
    """Filters log records based on a parameter in the `extra` dictionary."""
    if not hasattr(record, "log_to_stderr") or record.log_to_stderr is None:
        return True

    return record.log_to_stderr


def get_component_logger_file_path() -> Optional[str]:
    """Returns the relative file path for the Serve logger, if it exists.

    If a logger was configured through configure_component_logger() for the Serve
    component that's calling this function, this returns the location of the log file
    relative to the ray logs directory.
    """
    logger = logging.getLogger(SERVE_LOGGER_NAME)
    for handler in logger.handlers:
        if isinstance(handler, logging.handlers.RotatingFileHandler):
            absolute_path = handler.baseFilename
            ray_logs_dir = ray._private.worker._global_node.get_logs_dir_path()
            if absolute_path.startswith(ray_logs_dir):
                return absolute_path[len(ray_logs_dir) :]


def configure_component_logger(
    *,
    component_name: str,
    component_id: str,
    component_type: Optional[str] = None,
    log_level: int = logging.INFO,
    max_bytes: Optional[int] = None,
    backup_count: Optional[int] = None,
):
    """Returns a logger to be used by a Serve component.

    The logger will log using a standard format to make components identifiable
    using the provided name and unique ID for this instance (e.g., replica ID).

    This logger will *not* propagate its log messages to the parent logger(s).
    """
    logger = logging.getLogger(SERVE_LOGGER_NAME)
    logger.propagate = False
    logger.setLevel(log_level)
    if os.environ.get(DEBUG_LOG_ENV_VAR, "0") != "0":
        logger.setLevel(logging.DEBUG)

    factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        request_context = ray.serve.context._serve_request_context.get()
        record = factory(*args, **kwargs)
        if request_context.route:
            record.route = request_context.route
        if request_context.request_id:
            record.request_id = request_context.request_id
        if request_context.app_name:
            record.app_name = request_context.app_name
        return record

    logging.setLogRecordFactory(record_factory)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ServeFormatter(component_name, component_id))
    stream_handler.addFilter(log_to_stderr_filter)
    logger.addHandler(stream_handler)

    logs_dir = os.path.join(
        ray._private.worker._global_node.get_logs_dir_path(), "serve"
    )
    os.makedirs(logs_dir, exist_ok=True)
    if max_bytes is None:
        max_bytes = ray._private.worker._global_node.max_bytes
    if backup_count is None:
        backup_count = ray._private.worker._global_node.backup_count
    if component_type is not None:
        component_name = f"{component_type}_{component_name}"
    log_file_name = LOG_FILE_FMT.format(
        component_name=component_name, component_id=component_id
    )
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir, log_file_name),
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(ServeFormatter(component_name, component_id))
    logger.addHandler(file_handler)


class LoggingContext:
    """
    Context manager to manage logging behaviors within a particular block, such as:
    1) Overriding logging level

    Source (python3 official documentation)
    https://docs.python.org/3/howto/logging-cookbook.html#using-a-context-manager-for-selective-logging # noqa: E501
    """

    def __init__(self, logger, level=None):
        self.logger = logger
        self.level = level

    def __enter__(self):
        if self.level is not None:
            self.old_level = self.logger.level
            self.logger.setLevel(self.level)

    def __exit__(self, et, ev, tb):
        if self.level is not None:
            self.logger.setLevel(self.old_level)
