from http import HTTPStatus


class ClientException(Exception):

    def __init__(self, status: HTTPStatus, error_message: str):
        super(ClientException, self).__init__(
            f"ClientException[{status}]: {error_message}"
        )
        self.status = status
        self.error_message = error_message
