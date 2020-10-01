from gevent import spawn, joinall

from .http import request, Response, Method
from .async_request import AsyncRequest


class Client:
    __slots__ = (
        '_in_context',
        '_requests'
    )

    def __init__(self):
        self._in_context = False
        self._requests = []
    
    def __enter__(self):
        self._in_context = True
        return self
    
    def __exit__(self, *args, **kwargs):
        if not self._requests:
            return
        joinall([
            i.greenlet
            for i in self._requests
            if not i.is_done
        ])
    
    def get(self, url, **kwargs) -> AsyncRequest:
        req = AsyncRequest(spawn(request, url, method=Method.GET))
        if self._in_context:
            self._requests.append(req)
        return req

    def post(self) -> AsyncRequest:
        req = AsyncRequest(spawn(request, url, method=Method.POST))
        if self._in_context:
            self._requests.append(req)
        return req
    
    def put(self) -> AsyncRequest:
        req = AsyncRequest(spawn(request, url, method=Method.PUT))
        if self._in_context:
            self._requests.append(req)
        return req
