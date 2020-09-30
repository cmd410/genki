from gevent import spawn, Greenlet

from .http import request, Responce, Method


class Client:
    def __init__(self):
        pass
    
    def get(self, url, **kwargs) -> Greenlet:
        return spawn(request, url, method=Method.GET)

    def post(self) -> Greenlet:
        return spawn(request, url, method=Method.POST)
    
    def put(self) -> Greenlet:
        return spawn(request, url, method=Method.PUT)
