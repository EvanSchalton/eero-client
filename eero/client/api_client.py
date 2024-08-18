import json
from http import HTTPStatus
from logging import getLogger
from typing import Any

import requests

from ..exceptions import ClientException
from .models import ErrorMeta

logger = getLogger("eero")

API_VERSION = "2.2"


class APIClient(object):
    API_ENDPOINT = "https://api-user.e2ro.com/{}/{}"

    def _parse_response(self, action, response) -> dict[str, Any]:
        data = json.loads(response.text)
        logger.debug("Response for %s: %s", action, data)
        try:
            if data["meta"]["code"] not in [
                HTTPStatus.OK,
                HTTPStatus.CREATED,
                HTTPStatus.ACCEPTED,
            ]:
                client_exception = ClientException(
                    data["meta"]["code"], data["meta"].get("error", "Unknown Error")
                )
                logger.error(client_exception)

                try:
                    ErrorMeta.model_validate(data)
                    return data
                except Exception:
                    raise client_exception
        except ClientException as e:
            raise e
        except Exception as e:
            logger.error("KeyError - Failed to parse response: %s [%s]", data, e)
            try:
                raise ClientException(
                    data.get("result", {}).get("error", {}).get("requestId"),
                    data.get("result", {}).get("error", {}).get("message"),
                ) from e
            except KeyError:
                raise ClientException(
                    data.get("meta", {}).get("code", HTTPStatus.INTERNAL_SERVER_ERROR),
                    data.get("meta", {}).get("error", "Unknown Error"),
                ) from e
        return data.get("data", data.get("meta", {}))

    def request(self, method, action, **kwargs):
        response = requests.request(
            method, self.API_ENDPOINT.format(API_VERSION, action), **kwargs
        )
        return self._parse_response(action, response)

    def post(self, action, **kwargs):
        response = requests.post(
            self.API_ENDPOINT.format(API_VERSION, action), **kwargs
        )
        return self._parse_response(action, response)

    def get(self, action, **kwargs):
        response = requests.get(self.API_ENDPOINT.format(API_VERSION, action), **kwargs)
        return self._parse_response(action, response)
