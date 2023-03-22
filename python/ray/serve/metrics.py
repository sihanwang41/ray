from ray.util import metrics
from typing import Tuple, Optional, Dict, List
from ray.serve import context

DEPLOYMENT_TAG = "deployment"
REPLICA_TAG = "replica"


def _add_serve_metric_tags(tag_keys: Optional[Tuple[str]] = None):
    """Add serve context tags to the tag_keys"""
    if DEPLOYMENT_TAG in tag_keys:
        raise ValueError(f"'{DEPLOYMENT_TAG}' tag is reserved for Ray Serve metrics")
    if REPLICA_TAG in tag_keys:
        raise ValueError(f"'{REPLICA_TAG}' tag is reserved for Ray Serve metrics")
    # Get serve tag inserted:
    if tag_keys:
        tag_keys = (DEPLOYMENT_TAG, REPLICA_TAG) + tag_keys
    else:
        tag_keys = (DEPLOYMENT_TAG, REPLICA_TAG)
    return tag_keys


def _add_serve_metric_default_tags(default_tags: Dict[str, str]):
    """Add serve context tags and values to the default_tags"""
    if DEPLOYMENT_TAG in default_tags:
        raise ValueError(f"'{DEPLOYMENT_TAG}' tag is reserved for Ray Serve metrics")
    if REPLICA_TAG in default_tags:
        raise ValueError(f"'{REPLICA_TAG}' tag is reserved for Ray Serve metrics")
    default_tags[DEPLOYMENT_TAG] = context.REPLICA_DEPLOYMENT_NAME
    default_tags[REPLICA_TAG] = context.REPLICA_TAG_NAME
    return default_tags


class Counter(metrics.Counter):
    def __init__(
        self, name: str, description: str = "", tag_keys: Optional[Tuple[str]] = None
    ):
        tag_keys = _add_serve_metric_tags(tag_keys)
        super().__init__(name, description, tag_keys)
        self.set_default_tags({})

    def set_default_tags(self, default_tags: Dict[str, str]):
        super().set_default_tags(_add_serve_metric_default_tags(default_tags))


class Gauge(metrics.Gauge):
    def __init__(
        self, name: str, description: str = "", tag_keys: Optional[Tuple[str]] = None
    ):
        tag_keys = _add_serve_metric_tags(tag_keys)
        super().__init__(name, description, tag_keys)
        self.set_default_tags({})

    def set_default_tags(self, default_tags: Dict[str, str]):
        super().set_default_tags(_add_serve_metric_default_tags(default_tags))


class Histogram(metrics.Histogram):
    def __init__(
        self,
        name: str,
        description: str = "",
        boundaries: List[float] = None,
        tag_keys: Optional[Tuple[str]] = None,
    ):
        tag_keys = _add_serve_metric_tags(tag_keys)
        super().__init__(name, description, boundaries, tag_keys)
        self.set_default_tags({})

    def set_default_tags(self, default_tags: Dict[str, str]):
        super().set_default_tags(_add_serve_metric_default_tags(default_tags))
