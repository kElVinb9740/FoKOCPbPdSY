# 代码生成时间: 2025-09-12 17:20:12
import json
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError, NotFound

# 用户界面组件库应用
app = Sanic("UIComponentLibrary")

# 组件存储
components = {
    "button": "<button>Click me!</button>", 
    "input": "<input type='text' placeholder='Type here...'>", 
    "label": "<label>Enter your name:</label>"
}

# 组件库首页
@app.route("/")
async def index(request: Request):
    """
    显示用户界面组件库首页
    """
    return response.html("<h1>Welcome to UI Component Library</h1>")

# 获取组件详情
@app.route("/component/<name>", methods=["GET"])
async def get_component(request: Request, name: str):
    """
    根据组件名称获取组件详情
    """
    try:
        component = components.get(name)
        if component is None:
            raise NotFound("Component not found")
        return response.json({"name": name, "html": component})
    except Exception as e:
        raise ServerError(str(e))

# 错误处理
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: ServerError):
    """
    服务器错误处理
    """
    return response.json(
        {
            "error": "Internal Server Error",
            "message": str(exception)
        },
        status=500,
    )

@app.exception(NotFound)
async def handle_not_found(request: Request, exception: NotFound):
    """
    资源未找到错误处理
    """
    return response.json(
        {
            "error": "Not Found",
            "message": str(exception)
        },
        status=404,
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)