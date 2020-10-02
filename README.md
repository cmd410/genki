# GENKI - gevent based http library

**Genki** - http library built on top of [gevent](http://www.gevent.org) sockets, which allow to perform asynchronous requests.

It is still in **very early stages of development**. Please, do not use it for real production.

> **Genki** does not monkey patch anything, don't you worry, your stdlib is safe. Its up to you to patch it.

## Example usage

```python
from genki import Client

if __name__ == '__main__':
    c = Client()  # Create instance of client
    
    # .result() waits for answer while your program can do other stuff
    response = c.get('http://example.com/').result()   
    print(response.body)
```
or
```python
from genki import Client


if __name__ == '__main__':
    # Creating context for client
    with Client(timeout=2) as c:
        # Start asynchronous requsets
        req2 = c.get('https://example.com')
        ...

    # When context exits client makes sure all requests are completed
    print(req2.result())  # Does not wait, request already finished
```

## Future plans

- Support for URL parameters
- Support more standards

## Contributing

If you notice some strange behavior with this library, feel free to [leave an issue](https://github.com/cmd410/genki/issues) describing the problem(make sure your issue haven't already been submitted). If you happen to know how to fix an issue, pull requests are also welcome.

