import importlib.util
import inspect

import pytest
from pboot import Pboot
from pboot import make_response

from pboot_caching import Cache
from pboot_caching import CachedResponse
from pboot_caching.backends import FileSystemCache
from pboot_caching.backends import MemcachedCache
from pboot_caching.backends import NullCache
from pboot_caching.backends import RedisCache
from pboot_caching.backends import RedisSentinelCache
from pboot_caching.backends import SASLMemcachedCache
from pboot_caching.backends import SimpleCache
from pboot_caching.backends import SpreadSASLMemcachedCache

# pylibmc doesn't have any wheels for python > 3.11
pylibmc_available = False
try:
    importlib.util.find_spec("pylibmc")
except ImportError:
    pylibmc_available = False


cache_types = [
    FileSystemCache,
    MemcachedCache,
    NullCache,
    RedisCache,
    RedisSentinelCache,
    SimpleCache,
]

if pylibmc_available:
    cache_types.append(SASLMemcachedCache)
    cache_types.append(SpreadSASLMemcachedCache)


@pytest.fixture
def app():
    app_ = Pboot(__name__)

    return app_


@pytest.mark.parametrize(
    "cache_type",
    (cache_types),
)
def test_init_nullcache(cache_type, app, tmp_path):
    extra_config = {
        FileSystemCache: {
            "CACHE_DIR": tmp_path,
        },
        MemcachedCache: {
            "CACHE_MEMCACHED_SERVERS": ["127.0.0.1:11212"],
        },
        RedisCache: {
            "CACHE_REDIS_PORT": 6360,
        },
        SASLMemcachedCache: {
            "CACHE_MEMCACHED_SERVERS": ["127.0.0.1:11212"],
            "CACHE_MEMCACHED_USERNAME": "test",
            "CACHE_MEMCACHED_PASSWORD": "test",
        },
        SpreadSASLMemcachedCache: {
            "CACHE_MEMCACHED_SERVERS": ["127.0.0.1:11212"],
            "CACHE_MEMCACHED_USERNAME": "test",
            "CACHE_MEMCACHED_PASSWORD": "test",
        },
    }
    app.config["CACHE_TYPE"] = "pboot_caching.backends." + cache_type.__name__
    app.config.update(extra_config.get(cache_type, {}))
    cache = Cache(app=app)

    assert isinstance(app.extensions["cache"][cache], cache_type)


def test_cached_response_init_is_typed():
    """Regression test for issue #628.

    ``CachedResponse.__init__`` must declare a return type and parameter
    types so that mypy ``--strict`` doesn't flag construction in typed
    code with ``[no-untyped-call]``. See
    https://github.com/pallets-eco/flask-caching/issues/628.
    """
    sig = inspect.signature(CachedResponse.__init__)
    # __init__ should declare ``-> None`` rather than be untyped.
    # inspect.signature returns the literal ``None`` for ``-> None``.
    assert sig.return_annotation is None, (
        f"CachedResponse.__init__ return annotation is {sig.return_annotation!r}; "
        "expected None"
    )
    # All non-self parameters should carry an annotation.
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        assert param.annotation is not inspect.Parameter.empty, (
            f"CachedResponse.__init__ parameter {name!r} has no annotation"
        )


def test_cached_response_construction_with_pboot_response():
    """Sanity check that CachedResponse still wraps a pboot Response."""
    app = Pboot(__name__)
    with app.test_request_context():
        resp = make_response("hi")
        cached = CachedResponse(resp, 10)
    assert cached.timeout == 10
    assert cached.get_data(as_text=True) == "hi"
