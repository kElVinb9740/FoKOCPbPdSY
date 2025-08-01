# 代码生成时间: 2025-08-01 20:22:39
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
import ujson as json
from sanic.log import logger

# 全局缓存字典，用于存储缓存数据
cache = {}

# 获取缓存中的数据，如果数据不存在则返回None
def get_cache(key):
    """
    Get cached data for a given key.
    :param key: The key to look for in the cache.
    :return: The cached data if present, otherwise None.
    """
    return cache.get(key)

# 将数据添加到缓存中
def set_cache(key, value, expire=None):
    """
    Set data to the cache with an optional expiration time.
    :param key: The key to store the data under.
    :param value: The data to store in the cache.
    :param expire: The time in seconds after which the data expires.
    """
    cache[key] = {'value': value, 'expire': expire}
    logger.info(f"Data added to cache with key: {key}. Expiry: {expire}")

# 检查缓存中的数据是否过期，并清理过期的数据
def check_cache_expiration():
    """
    Check for expired cache items and remove them.
    """
    current_time = asyncio.get_running_loop().time()
    for key, item in list(cache.items()):
        if item['expire'] is not None and item['expire'] < current_time:
            del cache[key]
            logger.info(f"Expired data removed from cache with key: {key}.")

# Sanic 应用实例化
app = Sanic('CachingService')

# 缓存刷新任务（异步定时任务），用于清理过期缓存
@asyncio.coroutine
def refresh_cache_task(request):
    """
    Async task to refresh cache by removing expired items.
    :param request: The request object.
    """
    check_cache_expiration()
    loop = asyncio.get_event_loop()
    loop.call_later(10, refresh_cache_task)  # 每10秒检查一次过期缓存

# 在启动时添加异步定时任务
@app.listener('after_server_start')
def add_refresh_cache_task(app, loop):
    loop.call_later(10, refresh_cache_task)

# 获取缓存数据的端点
@app.route('/cache/<key>', methods=['GET'])
async def get_cached_data(request, key):
    """
    Get cached data for a given key.
    :param request: The request object.
    :param key: The caching key.
    :return: The cached data.
    """
    cached_data = get_cache(key)
    if cached_data:
        return response.json(cached_data['value'])
    else:
        raise NotFound("Cached data not found.")

# 设置缓存数据的端点
@app.route('/cache/<key>', methods=['POST'])
async def set_cached_data(request, key):
    """
    Set data to the cache for a given key.
    :param request: The request object.
    :param key: The caching key.
    """
    try:
        data = request.json
        expire = data.get('expire', None)
        set_cache(key, data['value'], expire)
        return response.json({'message': 'Data added to cache successfully.'})
    except Exception as e:
        raise ServerError("Failed to add data to cache.", e)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)