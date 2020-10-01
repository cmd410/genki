from gevent import Greenlet

from .http import Response


class AsyncRequest:
    def __init__(self, greenlet: Greenlet):
        self.greenlet = greenlet

    def result(self) -> Response:
        return self.greenlet.get()
    
    @property
    def is_done(self):
        return self.greenlet.ready()