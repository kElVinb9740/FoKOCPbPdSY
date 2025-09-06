# 代码生成时间: 2025-09-07 06:46:47
import aiohttp
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import json
from urllib.parse import urlparse, parse_qs


# 定义全局变量
USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


# 初始化Sanic应用
app = Sanic("WebScraper")


# 定义错误处理
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    return response.json({"error": "Internal Server Error"}, status=500)

@app.exception(NotFound)
async def handle_not_found(request: Request, exception: NotFound):
    return response.json({"error": "Not Found"}, status=404)


# 定义抓取网页内容的函数
async def fetch_web_content(url: str):
    # 解析URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.netloc:
        raise ValueError("Invalid URL")

    # 使用aiohttp进行异步HTTP请求
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=USER_AGENT) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: HTTP {response.status} received"
        except aiohttp.ClientError as e:
            raise ServerError(f"Network error: {e}")


# 定义Sanic路由以抓取网页内容
@app.route("/scraper", methods=["GET"])
async def scraper(request: Request):
    # 获取查询参数
    query_params = parse_qs(request.query_string.decode())
    url = query_params.get("url", [None])[0]
    if not url:
        return response.json({"error": "URL parameter is missing"})

    try:
        # 调用抓取网页内容的函数
        content = await fetch_web_content(url)
        return response.json({"content": content})
    except ValueError as ve:
        return response.json({"error": str(ve)})
    except ServerError as se:
        return response.json({"error": str(se)})


# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)