from logging import getLogger
from typing import Optional

from gevent import joinall

from .http import Headers
from .async_request import AsyncRequest
from .http_requests import (get, post, put, patch,
                            trace, options, delete,
                            connect, head)

logger = getLogger('genki')


class Client:
    __slots__ = (
        'timeout',
        '_requests'
    )

    def __init__(self, timeout=None):
        self.timeout = timeout
        self._requests = []

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.collect()

    def collect(self, timeout=None):
        """Wait till all previously defined requests are finished
        """
        if not self._requests:
            return
        joinall([
            i.async_result
            for i in self._requests
            if not i.is_done
        ])

    def get(self,
            url,
            data=None,
            params=None,
            headers: Headers = Headers(),
            timeout: Optional[float] = None
            ) -> AsyncRequest:
        timeout = timeout or self.timeout
        req = get(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def post(self,
             url,
             data=None,
             params=None,
             headers: Headers = Headers(),
             timeout: Optional[float] = None
             ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = post(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def patch(self,
              url,
              data=None,
              params=None,
              headers: Headers = Headers(),
              timeout: Optional[float] = None
              ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = patch(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def put(self,
            url,
            data=None,
            params=None,
            headers: Headers = Headers(),
            timeout: Optional[float] = None
            ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = put(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def delete(self,
               url,
               data=None,
               params=None,
               headers: Headers = Headers(),
               timeout: Optional[float] = None
               ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = delete(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def options(self,
                url,
                data=None,
                params=None,
                headers: Headers = Headers(),
                timeout: Optional[float] = None
                ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = options(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def head(self,
             url,
             data=None,
             params=None,
             headers: Headers = Headers(),
             timeout: Optional[float] = None
             ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = head(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def trace(self,
              url,
              data=None,
              params=None,
              headers: Headers = Headers(),
              timeout: Optional[float] = None
              ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = trace(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req

    def connect(self,
                url,
                data=None,
                params=None,
                headers: Headers = Headers(),
                timeout: Optional[float] = None
                ) -> AsyncRequest:
        timeout = timeout or self.timeout

        req = connect(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout)
        self._requests.append(req)
        return req
