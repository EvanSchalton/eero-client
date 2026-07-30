import json
import os
from copy import copy
from logging import getLogger
from pathlib import Path
from typing import Any

from pydantic import BaseModel, TypeAdapter, ValidationError

from ..models import ErrorMeta
from .routes import GET_RESOURCES, POST_RESOURCES, Resource

logger = getLogger("eero")

DEBUGGING_PATH = (
    Path(raw_debugging_path)
    if (raw_debugging_path := os.environ.get("DEBUGGING_PATH", None))
    else None
)
logger.debug("DEBUGGING_PATH: %s", DEBUGGING_PATH)


def _write_debug_payload(action: str, result: Any) -> None:
    """Write an explicitly requested raw response with restricted permissions."""
    if DEBUGGING_PATH is None:
        return

    DEBUGGING_PATH.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        DEBUGGING_PATH.chmod(0o700)
    output_path = DEBUGGING_PATH / f"{action}.json"
    file_descriptor = os.open(
        output_path,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )
    with os.fdopen(file_descriptor, "w") as output_file:
        json.dump(result, output_file, indent=2)
    if os.name != "nt":
        output_path.chmod(0o600)


def _validation_error_summary(error: ValidationError) -> list[dict[str, Any]]:
    """Return validation diagnostics without values or validator messages."""
    return [
        {"location": item["loc"], "type": item["type"]}
        for item in error.errors(
            include_url=False,
            include_context=False,
            include_input=False,
        )
    ]


def make_method(method: str, action: str, resource: Resource, **kwargs: Any):
    method = copy(method)
    action = copy(action)
    resource = copy(resource)

    logger.debug("%s: %s (%s)", method, action, resource)

    def func(
        self, **kwargs: str
    ) -> None | dict[str, Any] | BaseModel | list[BaseModel]:
        url, model = resource
        logger.debug("%s: %s (%s)", action, url, model)
        for key, value in kwargs.items():
            url = url.replace(f"<{key}>", str(value))

        result = self.refreshed(lambda: self.client.request(method, url))

        if model is not None:
            try:
                _write_debug_payload(action, result)

                logger.debug("Validating response for %s", action)
                logger.debug("Model: %s", model)
                logger.debug("Model Type: %s", type(model))

                try:
                    if isinstance(result, list):
                        return TypeAdapter(
                            list[type(model)]  # type: ignore
                        ).validate_python(result)
                    return model.model_validate(result)  # type: ignore
                except ValidationError:
                    raise
                except Exception as e:
                    logger.error(
                        "[%s] Failed to marshal response (%s)",
                        action,
                        type(e).__name__,
                    )
                    raise

            except ValidationError as e:
                if model == ErrorMeta:
                    logger.warning("Not Implemented: %s (expected error)", action)
                    return result
                logger.error(
                    "Failed to validate %s: %s",
                    action,
                    _validation_error_summary(e),
                )
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
