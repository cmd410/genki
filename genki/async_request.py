from typing import Union

from gevent import Greenlet
from gevent.event import AsyncResult

from .http import Response


class AsyncRequest:
    def __init__(self, greenlet: Greenlet):
        self.async_result: AsyncResult = AsyncResult()
        greenlet.link(self.async_result)

    def result(self) -> Union[Response, Exception]:
        self.async_result.wait()
        return self.async_result.value or self.async_result.exception

    @property
    def is_done(self):
        return self.async_result.ready()
