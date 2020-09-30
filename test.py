from unittest import TestCase, main

from genki.http.constants import Protocol
from genki.http.util import parse_url
from genki.http.exceptions import InvalidURL


class RequestPreparations(TestCase):
    def test_url(self):
        
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
            with self.subTest(url=url):
                self.assertEqual(parse_url(url), result)
    
    def test_invalid_urls(self):
        invalid_cases = [
            'https://',
            '/',
            '',
            'example.com:',
            ':example.com',
            'http://example.com:',
            'http://:example.com'
        ]

        for i in invalid_cases:
            with self.subTest(url=i):
                self.assertRaises(InvalidURL, parse_url, i)
        
        with self.subTest(url='htps://example.com/'):
            self.assertRaises(ValueError, parse_url, 'htps://example.com/')


if __name__ == '__main__':
    main()
