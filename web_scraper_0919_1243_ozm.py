# 代码生成时间: 2025-09-19 12:43:18
import asyncio
from sanic import Sanic
from sanic.response import json, text
from requests_html import HTMLSession
from urllib.parse import urljoin
import re

# 定义一个简单的网页抓取工具，使用Sanic框架
app = Sanic("WebScraper")

# HTML会话对象，用于网页内容抓取
session = HTMLSession()

# 抓取网页内容的函数
async def fetch_web_content(url):
    """
    Fetches the content of a webpage.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The content of the webpage.
    Raises:
        Exception: If there is an error fetching the webpage.
    """
    try:
        response = await loop.run_in_executor(None, session.get, url)
        response.raise_for_status()  # 检查响应状态码
        return response.html.html  # 返回网页内容
    except Exception as e:
        raise Exception(f"Failed to fetch webpage: {str(e)}")

# 定义一个Sanic视图，用于处理抓取网页内容的请求
@app.route("/fetch/<url:re:https?://[^/]+>/", methods=["GET"])
async def fetch_content(request, url):
    """
    Fetches the content of a webpage based on the provided URL.

    Args:
        request: The Sanic request object.
        url (str): The URL of the webpage to fetch.

    Returns:
        Response: A JSON response with the webpage content.
    """
    content = await fetch_web_content(url)
    return json(content)

# 定义一个Sanic视图，用于处理抓取网页内容并返回文本的请求
@app.route("/fetch_text/<url:re:https?://[^/]+>/", methods=["GET"])
async def fetch_text_content(request, url):
    """
    Fetches the content of a webpage as text based on the provided URL.

    Args:
        request: The Sanic request object.
        url (str): The URL of the webpage to fetch.

    Returns:
        Response: A text response with the webpage content.
    """
    content = await fetch_web_content(url)
    return text(content)

# 定义一个Sanic视图，用于处理抓取网页内容并提取特定标签的请求
@app.route("/fetch_tag/<url:re:https?://[^/]+>/<tag:re:[a-z]+>/", methods=["GET"])
async def fetch_tag_content(request, url, tag):
    """
    Fetches the content of a webpage and extracts the specified HTML tag.

    Args:
        request: The Sanic request object.
        url (str): The URL of the webpage to fetch.
        tag (str): The HTML tag to extract.

    Returns:
        Response: A JSON response with the extracted content.
    """
    content = await fetch_web_content(url)
    matches = content.find("<{0}>".format(tag), 0)
    if matches:
        return json(content.html.find("<{0}>".format(tag)))
    else:
        return json({})

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)