# 代码生成时间: 2025-08-27 06:34:49
import aiohttp
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound, abort
from sanic.request import Request
from sanic.response import json
from urllib.parse import urlparse
import asyncio

# 定义一个函数来检查URL是否有效
async def is_valid_url(url: str) -> bool:
    """
    检查给定的URL是否有效。

    :param url: 需要检查的URL字符串
    :return: 如果URL有效，则返回True，否则返回False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# 创建Sanic应用
app = Sanic("URL Validator Service")

# 定义路由处理函数
@app.route("/validate", methods=["GET"])
async def validate_url(request: Request):
    """
    验证请求参数中的URL是否有效。

    :param request: 请求对象
    :return: JSON响应，包含URL有效性的结果
    """
    url = request.args.get("url")
    if url:
        is_valid = await is_valid_url(url)
        return json({"url": url, "isValid": is_valid})
    else:
        abort(400, "URL parameter is missing")

# 启动Sanic应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)