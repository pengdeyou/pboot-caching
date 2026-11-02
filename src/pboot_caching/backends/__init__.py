"""
pboot_caching.backends
~~~~~~~~~~~~~~~~~~~~~~

Various caching backends.

:copyright: (c) 2018 by Peter Justin.
:copyright: (c) 2010 by Thadeus Burgess.
:license: BSD, see LICENSE for more details.
"""

from pboot_caching.backends.base import BaseCache
from pboot_caching.backends.filesystemcache import FileSystemCache
from pboot_caching.backends.memcache import MemcachedCache
from pboot_caching.backends.memcache import SASLMemcachedCache
from pboot_caching.backends.memcache import SpreadSASLMemcachedCache
from pboot_caching.backends.nullcache import NullCache
from pboot_caching.backends.rediscache import RedisCache
from pboot_caching.backends.rediscache import RedisClusterCache
from pboot_caching.backends.rediscache import RedisSentinelCache
from pboot_caching.backends.simplecache import SimpleCache

__all__ = (
    "BaseCache",
    "NullCache",
    "SimpleCache",
    "FileSystemCache",
    "RedisCache",
    "RedisSentinelCache",
    "RedisClusterCache",
    "MemcachedCache",
    "SASLMemcachedCache",
    "SpreadSASLMemcachedCache",
)
