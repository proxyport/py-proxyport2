from .proxyport2 import instance
from .__version__ import __version__

__all__ = ['get_proxy', 'set_api_key', 'set_user_agent', '__version__']


def get_proxy():
    return instance.get_proxy()


def set_api_key(api_key):
    instance.set_api_key(api_key)


def set_user_agent(user_agent):
    instance.set_user_agent(user_agent)
