# Proxy Module

This module provides a simple way to handle proxies in Python. It includes two main classes: `ProxyType` and `Proxy`.

## ProxyType

`ProxyType` is a `(str, Enum)` enumeration that defines four types of proxies:

- `HTTP` (`http`) — **default**
- `SOCKS4` (`socks4`)
- `SOCKS5` (`socks5`) — DNS resolved locally
- `SOCKS5h` (`socks5h`) — DNS resolved on the proxy server

## Proxy

#### `Proxy` is a class that represents a proxy. It includes the following attributes:

- `ip`: The IP address of the proxy.
- `port`: The port number of the proxy.
- `username`: The username for the proxy (if required).
- `password`: The password for the proxy (if required).
- `type`: The type of the proxy, as defined by the `ProxyType` enumeration.

#### The `Proxy` class includes these properties:

- `url`: This property returns the URL of the proxy (no credentials).
- `full_url`: This property returns the full URL of the proxy, including the username and password (if they exist).
- `one_line_proxy`: This property returns a one-line representation of the proxy, including the username and password (if they exist).
- `requests`: This property returns a dictionary that can be used as the `proxies` parameter in a `requests` call.
- `aiohttp`: This property returns a dictionary that can be spread into an `aiohttp` call (e.g. `session.get(url, **proxy.aiohttp)`). Credentials are embedded in the proxy URL — aiohttp [supports this natively](https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support).


#### The `Proxy` class also includes several methods:

- `load(raw_proxy)`: This method takes a raw proxy string and parses it to fill the attributes of the `Proxy` object.
- `id()`: This method returns a unique identifier for the proxy, which is a combination of the IP and port, with the dots in the IP removed.

## Installation

You can install the module using `pip`:

```bash
pip install git+https://github.com/niriter/Proxy.git
```

## Usage

Here is a basic example of how to use the `Proxy` class:

```python
from proxy import Proxy, ProxyType

# Create a new Proxy object
p = Proxy('192.168.1.1:8080', ProxyType.HTTP)

print(p.url)        # http://192.168.1.1:8080
print(p.aiohttp)    # {'proxy': 'http://192.168.1.1:8080'}
```

## Input formats

The constructor accepts several input forms, detected automatically:

```python
Proxy('192.168.1.1:8080')                              # host:port
Proxy('192.168.1.1:8080:alice:secret')                 # host:port:user:pass (legacy)
Proxy('http://alice:secret@192.168.1.1:8080')          # URL with scheme
Proxy('alice:secret@192.168.1.1:8080')                 # URL without scheme
```

For non-standard field orders, pass an explicit `schema`:

```python
Proxy('alice:secret:192.168.1.1:8080', schema='user:pass:host:port')
Proxy('8080,192.168.1.1,secret,alice', schema='port,ip,password,username')
```

Schema separator is whatever non-alphanumeric character is used in the schema
itself. Allowed field names: `host`/`ip`, `port`, `user`/`username`, `pass`/`password`.