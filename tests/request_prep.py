from unittest import TestCase
from itertools import product

from genki.http.request import RequestBuilder
from genki.http.constants import Protocol
from genki.http.exceptions import InvalidURL


class RequestPreparations(TestCase):
    def test_url(self):
        """Check that url parses correctly
        """
        cases = [
            (
                'example.com',
                (Protocol.HTTP, 'example.com', '/', 80)),
            (
                'http://example.com',
                (Protocol.HTTP, 'example.com', '/', 80)),
            (
                'https://example.com',
                (Protocol.HTTPS, 'example.com', '/', 443)),
            
            (
                'example.com/',
                (Protocol.HTTP, 'example.com', '/', 80)),
            (
                'http://example.com/',
                (Protocol.HTTP, 'example.com', '/', 80)),
            (
                'https://example.com/',
                (Protocol.HTTPS, 'example.com', '/', 443)),

            (
                'example.com/some/path',
                (Protocol.HTTP, 'example.com', '/some/path', 80)),
            (
                'http://example.com/some/path',
                (Protocol.HTTP, 'example.com', '/some/path', 80)),
            (
                'https://example.com/some/path',
                (Protocol.HTTPS, 'example.com', '/some/path', 443)),

            (
                'example.com:8080/some/path',
                (Protocol.HTTP, 'example.com', '/some/path', 8080)),
            (
                'http://example.com:8080/some/path',
                (Protocol.HTTP, 'example.com', '/some/path', 8080)),
            (
                'https://example.com:8080/some/path',
                (Protocol.HTTPS, 'example.com', '/some/path', 8080)),
        ]

        for url, result in cases:
            protocol, host, path, port = result
            with self.subTest(url=url):
                req_builder = RequestBuilder(url)
                self.assertEqual(req_builder.protocol, protocol)
                self.assertEqual(req_builder.host, host)
                self.assertEqual(req_builder.path, path)
                self.assertEqual(req_builder.port, port)

    def test_invalid_urls(self):
        """Make sure invalid urls will raise an error
        """
        invalid_cases = [
            'https://',
            '/',
            '',
            'example.com:',
            ':example.com',
            'http://example.com:',
            'http://:example.com'
        ]

        for url in invalid_cases:
            with self.subTest(url=url):
                self.assertRaises(InvalidURL, RequestBuilder, url)

    def test_to_bytes(self):
        """Test that request converts to bytes correctly
        """
        s = 'GET {path} HTTP/1.1\r\nHost: {host}\r\n'

        hosts = [
            'example.com',
            'http://example.com',
            'https://example.com',
            'http://example.com:8080'
        ]

        paths = [
            '/',
            '/some/path'
        ]

        for host, path in product(hosts, paths):
            url = host + path
            with self.subTest(url=url):
                req = RequestBuilder(url)
                req_body = s.format(host=hosts[0], path=path)
                self.assertEqual(req.to_bytes(), (req_body + '\r\n').encode())
