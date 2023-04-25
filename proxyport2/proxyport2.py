from datetime import datetime, timedelta
import json
import logging
import os
from random import choice
from urllib.request import urlopen, Request

from .__version__ import __version__

logger = logging.getLogger(__name__)


class ProxyPort:
    last_load = None
    warned = False
    api_url = 'https://api.proxy-port.com/scraping-proxy'
    user_agent = 'py-proxyport2/{}'.format(__version__)
    headers = {'User-Agent': user_agent}
    ttl_seconds = 5 * 60
    ttl_delta = timedelta(seconds=ttl_seconds)

    def __init__(self, api_key=None):
        self.log = logger
        self.new_proxy = list()
        self.known_proxy = dict()
        if not api_key:
            api_key = os.environ.get('PROXY_PORT_API_KEY')
        if api_key:
            self.set_api_key(api_key)
            self._load_proxy()

    def set_user_agent(self, user_agent):
        self.headers['User-Agent'] = '{} {}'.format(
            self.user_agent, user_agent)

    def set_api_key(self, api_key):
        self.headers['X-API-KEY'] = api_key

    def get_proxy(self):
        self._refresh()
        if not self.new_proxy:
            if not self.known_proxy:
                self.log.warning('Proxy list is empty')
                return
            return choice(list(self.known_proxy.keys()))
        proxy = self.new_proxy.pop(0)
        return proxy

    def get_proxy_list(self):
        self._refresh()
        return self.new_proxy

    def _load_proxy(self):
        if not self.headers.get('X-API-KEY'):
            raise AuthorizationError(
                '\nAPI key are not specified, '
                'call `set_api_key` before usage:\n\n'
                ' from proxyport2 import set_api_key, get_proxy\n\n'
                ' set_api_key(<API_KEY>)\n'
                ' print(get_proxy())\n'
            )
        try:
            response = urlopen(Request(self.api_url, headers=self.headers))
            response_data = json.load(response)
        except Exception as e:
            self._check_error(e)
            return
        if response_data.get('warning') and not self.warned:
            self.log.warning(response_data.get('warning'))
            self.warned = True

        self._proxy_list_gc()

        new_proxy = []
        for proxy in response_data.get('data'):
            if not self.known_proxy.get(proxy) or proxy in self.new_proxy:
                new_proxy.append(proxy)
            self.known_proxy[proxy] = datetime.now() + self.ttl_delta
        self.new_proxy = new_proxy
        self.last_load = datetime.now()

    def _proxy_list_gc(self):
        now = datetime.now()
        for address, ttl in list(self.known_proxy.items()):
            if now > ttl:
                del self.known_proxy[address]

    def _check_error(self, e):
        auth_failed = False
        msg = str(e)
        if hasattr(e, 'code'):
            if e.code == 401:
                auth_failed = True
                msg = (
                    'Invalid API key, visit '
                    'https://account.proxy-port.com/scraping to obtain new key'
                )
        self.log.error('Error on API call, {}'.format(msg))
        if auth_failed:
            raise AuthorizationError(msg)

    def _refresh(self):
        if (not self.last_load or
                self.last_load < datetime.now() - timedelta(seconds=60)):
            self._load_proxy()


class AuthorizationError(Exception):
    pass


instance = ProxyPort()
