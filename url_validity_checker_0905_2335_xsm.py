# 代码生成时间: 2025-09-05 23:35:30
import sanic
from sanic.response import json
from urllib.parse import urlparse, parse_qs
from sanic.exceptions import ServerError, NotFound
from sanic.log import logger
import requests
from requests.exceptions import RequestException

"""
URL链接有效性验证器
- 检查URL的格式是否正确
- 检查URL是否存在（ping）
"""

app = sanic.Sanic("UrlValidator")

@app.route("/check_url", methods=["POST"])
async def check_url(request):
    """
    检查URL链接的有效性
    
    参数:
        request: 包含URL的POST请求
    
    返回:
        状态码和URL检查结果
    """
    # 获取URL参数
    url = request.json.get("url", None)
    if not url:
        return json({
            "errors": [{"msg": "URL parameter is missing"}]},
            status=400,
        )
    
    # 检查URL格式
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return json({
                "errors": [{"msg": "Invalid URL format"}]},
                status=400,
            )
    except ValueError:
        return json({
            "errors": [{"msg": "Invalid URL format"}]},
            status=400,
        )
    
    # 检查URL是否存在（ping）
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        if response.status_code == 200:
            return json({
                "msg": "URL is valid and exists"},
                status=200,
            )
        else:
            return json({
                "errors": [{"msg": "URL does not exist or is not reachable"}]},
                status=404,
            )
    except RequestException as e:
        logger.error("Error checking URL: %s", str(e))
        return json({
            "errors": [{"msg": "URL check failed"}]},
            status=500,
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)