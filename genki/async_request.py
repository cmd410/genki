from typing import Union, Callable

from gevent import Greenlet
from gevent.event import AsyncResult

from .http import Response


class AsyncRequest:
    def __init__(self, greenlet: Greenlet):
        self.greenlet = greenlet
        self.async_result: AsyncResult = AsyncResult()
        greenlet.link(self.async_result)

    def result(self) -> Union[Response, Exception]:
        self.async_result.wait()
        return self.async_result.value or self.async_result.exception

    def bind(self,
             callback: Callable[[Union[Response, Exception]], None]) -> 'AsyncRequest':
        self.greenlet.link(lambda gl: callback(gl.get()))
        return self

    @property
    def is_done(self) -> bool:
        return self.async_result.ready()
