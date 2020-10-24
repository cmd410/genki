from gevent import socket

network_exceptions = (
    socket.timeout,
    socket.gaierror,
    ConnectionRefusedError,
    ConnectionError,
    ConnectionAbortedError,
    ConnectionResetError
)