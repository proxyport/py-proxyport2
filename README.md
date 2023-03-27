# Proxy Port SDK
`proxyport2` Python package provides interfaces to the <a href="https://proxy-port.com/en/scraping-proxy" target="_blank">Proxy Port</a> API.
## Prerequisites
To use this package you will need a free API key. Get your API key <a href="https://account.proxy-port.com/scraping" target="_blank">here</a>.
Detailed instructions <a href="https://proxy-port.com/en/scraping-proxy/getting-started" target="_blank">here</a>.
## Installation
Install via <a href="https://pip.pypa.io/" target="_blank">pip</a>:
```shell
$ pip install proxyport2
```
## Getting Started
Before you get your first proxy, you need to assign an API key.
This can be done either through an environment variable
```shell
$ export PROXY_PORT_API_KEY=<API_KEY>
```
or directly in the code.
```python
from proxyport2 import set_api_key, get_proxy

set_api_key('<API_KEY>') # here
print(get_proxy())

'139.180.281.313:3128'
```

Package can be used as module:
```shell
$ python -m proxyport2

['181.119.301.272:3128', ...]

```
