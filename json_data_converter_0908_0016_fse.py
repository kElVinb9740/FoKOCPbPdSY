# 代码生成时间: 2025-09-08 00:16:44
import json
from sanic import Sanic, response
from sanic.exceptions import ServerError, InvalidUsage, json_error_handler

# 创建一个Sanic应用
app = Sanic("JSON Data Converter")

# 错误处理装饰器
app.error_handler.add(http_exception, json_error_handler)

# 将JSON数据转换为Python字典的路由
@app.route("/convert", methods=["POST"])
async def convert_json(request):
    # 从请求中获取JSON数据
    data = request.json
    
    # 检查数据是否为None
    if data is None:
        # 返回错误信息
        return response.json({
            "error": "No JSON data provided"
        }, status=400)
    
    # 将JSON数据转换为Python字典
    python_dict = json.loads(json.dumps(data))
    
    # 返回转换后的Python字典
    return response.json(python_dict)

# 定义HTTP异常处理函数
def http_exception(request, exception):
    return json_error_handler(request, exception)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)