# Proxy Module

This module provides a simple way to handle proxies in Python. It includes two main classes: `ProxyType` and `Proxy`.

## ProxyType

`ProxyType` is an enumeration that defines three types of proxies:

- HTTP
- SOCKS4
- SOCKS5 (socks5h under the hood) **default

## Proxy

#### `Proxy` is a class that represents a proxy. It includes the following attributes:

- `ip`: The IP address of the proxy.
- `port`: The port number of the proxy.
- `username`: The username for the proxy (if required).
- `password`: The password for the proxy (if required).
- `type`: The type of the proxy, as defined by the `ProxyType` enumeration.

#### The `Proxy` class includes these properties:

- `url`: This property returns the URL of the proxy.
- `full_url`: This property returns the full URL of the proxy, including the username and password (if they exist).
- `auth`: This property returns an `aiohttp.BasicAuth` object if the proxy requires authentication, or `None` otherwise.
- `one_line_proxy`: This property returns a one-line representation of the proxy, including the username and password (if they exist).
- `requests`: This property returns a dictionary that can be used as the `proxies` parameter in a `requests` call.
- `aiohttp`: This property returns a dictionary that can be used as the `proxy` parameter in an `aiohttp` call.


#### The `Proxy` class also includes several methods:

- `load(raw_proxy)`: This method takes a raw proxy string and parses it to fill the attributes of the `Proxy` object.
- `is_work()`: This method checks if the proxy is working by making a request to 'https://api.my-ip.io/ip' and comparing the returned IP with the proxy's IP.
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

# Check if the proxy is working
if p.is_work():
    print('The proxy is working')
else:
    print('The proxy is not working')
```