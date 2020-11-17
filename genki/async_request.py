from typing import Union, Callable

from gevent import Greenlet
from gevent.event import AsyncResult

from .http import Response


class AsyncRequest:
    """Represents request that may not be finished yet
    """
    __slots__ = ('greenlet', 'async_result')

    def __init__(self, greenlet: Greenlet):
        self.greenlet = greenlet
        self.async_result: AsyncResult = AsyncResult()
        greenlet.link(self.async_result)

    def result(self, exc_raise=False) -> Union[Response, Exception]:
        """Wait for request to finish and return a result,
        which can be either Reponce object or Exception.

        If exc_raise is True, in case of Exception
        it will be immedeately raised.
        """
        self.async_result.wait()
        result = self.async_result.value or self.async_result.exception
        if exc_raise and isinstance(result, Exception):
            raise result
        return result

    def bind(self,
             callback: Callable[[Union[Response, Exception]], None]
             ) -> 'AsyncRequest':
        """Bind result of async request to a callable
        that accepts single argument - Responce or Exception
        """
        self.greenlet.link(lambda gl: callback(gl.get()))
        return self

    @property
    def is_done(self) -> bool:
        """True if request has been finished
        """
        return self.async_result.ready()
