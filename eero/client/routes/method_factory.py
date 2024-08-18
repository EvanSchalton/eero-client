import json
import os
from copy import copy
from logging import getLogger
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, TypeAdapter, ValidationError

from .routes import GET_RESOURCES, POST_RESOURCES, Resource
from ..models import ErrorMeta

logger = getLogger("eero")

DEBUGGING_PATH = (
    Path(raw_debugging_path)
    if (raw_debugging_path := os.environ.get("DEBUGGING_PATH", None))
    else None
)
if DEBUGGING_PATH:
    DEBUGGING_PATH.mkdir(parents=True, exist_ok=True)

logger.debug("DEBUGGING_PATH: %s", DEBUGGING_PATH)


def make_method(method: str, action: str, resource: Resource, **kwargs: Any):
    method = copy(method)
    action = copy(action)
    resource = copy(resource)

    logger.debug("%s: %s (%s)", method, action, resource)

    def func(self: Self, **kwargs: str) -> None | dict[str, Any] | BaseModel:
        url, model = resource
        logger.debug("%s: %s (%s)", action, url, model)
        for key, value in kwargs.items():
            url = url.replace("<{}>".format(key), str(value))

        result = self.refreshed(
            lambda: self.client.request(method, url, cookies=self._cookie_dict)
        )

        if model is not None:
            try:
                if DEBUGGING_PATH:
                    (DEBUGGING_PATH / f"{action}.json").write_text(
                        json.dumps(result, indent=2)
                    )

                if isinstance(result, list):
                    tpye_adatper = TypeAdapter(model)
                    return tpye_adatper.validate_python(result)
                if model == ErrorMeta:
                    logger.info(f"Not Implemented: {action} (expects error)")
                return model.model_validate(result)
            except ValidationError as e:
                if model == ErrorMeta:
                    logger.warn(f"Not Implemented: {action} (expected error)")
                    return result
                logger.error("Failed to validate %s: %s", action, e)
        return result

    return lambda self, **caller_kwargs: func(self, **kwargs, **caller_kwargs)


def create_get_method(action, resource):
    return property(
        lambda self: make_method(
            method="get",
            action=action,
            resource=resource,
            network_id=self.network_info.id,
        )(self)
    )


def create_post_method(action, resource):
    return lambda self, **kwargs: make_method(
        method="post",
        action=action,
        resource=resource,
        network_id=self.network_info.id,
    )(self, **kwargs)


# Create the methods dictionary
network_client_methods = {
    **{
        action: create_get_method(action, resource)
        for action, resource in GET_RESOURCES.items()
    },
    **{
        action: create_post_method(action, resource)
        for action, resource in POST_RESOURCES.items()
    },
}
