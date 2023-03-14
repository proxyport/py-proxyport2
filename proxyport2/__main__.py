import os

from .proxyport2 import instance

key = os.environ.get('PROXY_PORT_API_KEY')
if not key:
    key = input('Proxy Port API Key: ')
if not key:
    print('API Key are not specified')
else:
    instance.set_api_key(key)
    print(instance.get_proxy_list())
