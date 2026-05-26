# Proxy

Lightweight Python library for parsing and representing proxy connections. Zero runtime dependencies.

## Features

- Single `Proxy` value object with strong input validation
- Supports `HTTP`, `SOCKS4`, `SOCKS5`, `SOCKS5h`
- Auto-detects input format: `host:port`, `host:port:user:pass`, full URLs, URLs without scheme
- Explicit `schema=...` for non-standard field orders
- Hashable and comparable — usable in `set` / `dict`
- Password masked in `str()` and `repr()` — safe for logs
- Ready-to-spread dicts for `aiohttp` and `requests`

## Installation

```bash
pip install git+https://github.com/niriter/Proxy.git
```

For reproducible installs, pin to a tag:

```bash
pip install git+https://github.com/niriter/Proxy.git@v0.7
```

## Quick start

```python
from proxy import Proxy, ProxyType

p = Proxy('1.2.3.4:8080', ProxyType.HTTP)

print(p.url)      # http://1.2.3.4:8080
print(p.aiohttp)  # {'proxy': 'http://1.2.3.4:8080'}
```

### Use with HTTP clients

```python
# aiohttp
async with session.get(url, **proxy.aiohttp) as response:
    ...

# requests
requests.get(url, proxies=proxy.requests)
```

Credentials are embedded in the proxy URL — aiohttp supports this natively without `proxy_auth=`. See the [aiohttp docs](https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support).

## Input formats

The constructor auto-detects the input form:

```python
Proxy('1.2.3.4:8080')                          # host:port
Proxy('1.2.3.4:8080:alice:secret')             # host:port:user:pass
Proxy('socks5h://alice:secret@1.2.3.4:8080')   # URL with scheme
Proxy('alice:secret@1.2.3.4:8080')             # URL without scheme (http assumed)
```

Detection priority: explicit `schema=` → `://` in input → `@` in input → fallback to legacy colon-form. Anything that doesn't match raises `ValueError` with a clear message.

### Explicit schema

For non-standard field orders, pass `schema=`:

```python
Proxy('alice:secret:1.2.3.4:8080', schema='user:pass:host:port')
Proxy('8080,1.2.3.4,secret,alice', schema='port,ip,password,username')
```

The schema separator is whichever non-alphanumeric character appears in the schema string. Field names: `host`/`ip`, `port`, `user`/`username`, `pass`/`password`.

## Equality and hashing

Two proxies are equal when `(type, ip, port, username, password)` match. Instances are hashable:

```python
proxies = {Proxy(line) for line in open('proxies.txt')}  # dedup
```

> ⚠️ `Proxy` is mutable. Calling `.load()` after putting an instance into a set/dict makes the entry unreachable. Treat instances as values: build once, don't mutate.

## Logging safety

`str(proxy)` and `repr(proxy)` mask the password:

```python
p = Proxy('1.2.3.4:8080:alice:secret', ProxyType.SOCKS5h)

print(p)        # socks5h://alice:***@1.2.3.4:8080
print(repr(p))  # Proxy(socks5h://alice:***@1.2.3.4:8080)

logger.info(f'connecting through {p}')  # password never leaks
```

The real credentials remain available via `full_url`, `aiohttp`, and `requests` properties.

## API

### `ProxyType(str, Enum)`

| Member | Value | Notes |
|---|---|---|
| `HTTP` | `'http'` | default |
| `SOCKS4` | `'socks4'` | |
| `SOCKS5` | `'socks5'` | DNS resolved locally |
| `SOCKS5h` | `'socks5h'` | DNS resolved on the proxy server |

### `Proxy`

```python
Proxy(raw_proxy: str, proxy_type: ProxyType = ProxyType.HTTP, schema: str | None = None)
```

Raises `ValueError` on invalid input: empty string, missing host/port, port outside 1–65535, unknown schema field, etc.

**Attributes**

| Attribute | Type | Notes |
|---|---|---|
| `ip` | `str` | |
| `port` | `int` | validated 1–65535 |
| `username` | `str` | empty if no credentials |
| `password` | `str` | empty if no credentials |
| `type` | `ProxyType` | |

**Properties**

| Property | Returns |
|---|---|
| `url` | `'<scheme>://<ip>:<port>'` (no credentials) |
| `full_url` | `'<scheme>://<user>:<pass>@<ip>:<port>'` (credentials if present) |
| `one_line_proxy` | `'<user>:<pass>@<ip>:<port>'` |
| `requests` | `{'http': full_url, 'https': full_url}` |
| `aiohttp` | `{'proxy': full_url}` |

**Methods**

- `load(proxy: str, schema: str | None = None) -> None` — reparse with new input. Same priority rules as the constructor.

### `proxy.parser`

Low-level parsing functions, for use without constructing a `Proxy`:

```python
from proxy.parser import parse, parse_url, parse_legacy, parse_with_schema

host, port, user, password = parse('1.2.3.4:8080')
# ('1.2.3.4', 8080, '', '')
```

All return `tuple[str, int, str, str]` and raise `ValueError` on invalid input.

## Requirements

- Python 3.10+
- No runtime dependencies

## Versioning

Versions are derived from git tags via [hatch-vcs](https://github.com/ofek/hatch-vcs). Pin to a tag (`@vX.Y`) for reproducible installs.
