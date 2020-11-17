from logging import getLogger
from typing import Optional, Union, Mapping

from gevent import joinall

from .http import Headers
from .async_request import AsyncRequest
from .http_requests import (get, post, put, patch, delete)

logger = getLogger('genki')


class Client:
    """HTTP client class.

    Convinient way to wait for a bunch of requests to finish.
    Client.collect() method waits for all requests spawned by
    current client for finish.

    Can also be used as context manager. When client exits context,
    it automatically calls Client.collect() method.
    ```python
    with Client() as client:
        a = client.get('some address here')
        b = client.post('some other address')
        c = client.put('and another one')

    # Will not wait as all request are already finished
    results = [i.result() for i in (a, b, c)]
    ```

    Optionally timeout option can be passed into constructor
    to be applied to all requests of this client. Timeout
    can still be passed for individual requests and will take
    priority over Client's timeout.
    """
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
        self._requests.clear()

    def get(self,
            url,
            data=None,
            params: dict = None,
            headers: Union[Headers, Mapping] = Headers(),
            timeout: Optional[float] = None,
            follow_redirects: bool = True,
            redirects_limit: int = 5
            ) -> AsyncRequest:
        """Perform GET request
        """
        timeout = timeout or self.timeout
        req = get(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            redirects_limit=redirects_limit)
        self._requests.append(req)
        return req

    def post(self,
             url,
             data=None,
             params: dict = None,
             headers: Union[Headers, Mapping] = Headers(),
             timeout: Optional[float] = None,
             follow_redirects: bool = True,
             redirects_limit: int = 5
             ) -> AsyncRequest:
        """Perform POST request
        """
        timeout = timeout or self.timeout

        req = post(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            redirects_limit=redirects_limit)
        self._requests.append(req)
        return req

    def patch(self,
              url,
              data=None,
              params: dict = None,
              headers: Union[Headers, Mapping] = Headers(),
              timeout: Optional[float] = None,
              follow_redirects: bool = True,
              redirects_limit: int = 5
              ) -> AsyncRequest:
        """Perform PATCH request
        """
        timeout = timeout or self.timeout

        req = patch(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            redirects_limit=redirects_limit)
        self._requests.append(req)
        return req

    def put(self,
            url,
            data=None,
            params: dict = None,
            headers: Union[Headers, Mapping] = Headers(),
            timeout: Optional[float] = None,
            follow_redirects: bool = True,
            redirects_limit: int = 5
            ) -> AsyncRequest:
        """Perform PUT request
        """
        timeout = timeout or self.timeout

        req = put(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            redirects_limit=redirects_limit)
        self._requests.append(req)
        return req

    def delete(self,
               url,
               data=None,
               params: dict = None,
               headers: Union[Headers, Mapping] = Headers(),
               timeout: Optional[float] = None,
               follow_redirects: bool = True,
               redirects_limit: int = 5
               ) -> AsyncRequest:
        """Perform DELETE request
        """
        timeout = timeout or self.timeout

        req = delete(
            url=url,
            data=data,
            params=params,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            redirects_limit=redirects_limit)
        self._requests.append(req)
        return req
