# GENKI - gevent based http library

**Genki** - http library built on top of [gevent](http://www.gevent.org) sockets, which allow to perform asynchronous requests.

It is still in **very early stages of development**. Please, do not use it for real production.

> **Genki** does not monkey patch anything, don't you worry, your stdlib is safe. Its up to you to patch it.

## Example usage

```python
from genki import Client

if __name__ == '__main__':
    c = Client()
    responce = c.get('http://example.com/').get()
    print(responce.body)
```

## Future plans

- Get more convenient methods for accessing the world wide web 
- Support for URL parameters
- Automatically jsonify body data when needed
- Support more standards

## Contributing

If you notice some strange behavior with this library, feel free to [leave an issue](https://github.com/cmd410/genki/issues) describing the problem(make sure your issue haven't already been submitted). If you happen to know how to fix an issue, pull requests are also welcome.

