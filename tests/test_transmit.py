from unittest import TestCase, skipIf
from threading import Thread

from .test_server import app
from genki import Client


require_server = skipIf(
    app is None,
    '''Flask is not installed,
    \rtherefore no test server available''')


def start_server():
    Thread(target=app.run, daemon=True).start()


class TestTransmit(TestCase):
    def setUp(self):
        start_server()
        self.addr = 'localhost:5000'

    @require_server
    def test_basic_request(self):
        with Client(timeout=15) as client: 
            http_methods = (
                client.get,
                client.post,
                client.put,
                client.patch,
                client.delete)

            requests = dict()
            for method in http_methods:
                method_name = method.__name__.upper()
                requests[method_name] = method(self.addr+'/method')

        for responce, request in requests.items():
            result = request.result()
            self.assertNotIsInstance(result, Exception)
            self.assertEqual(result.body, responce)
