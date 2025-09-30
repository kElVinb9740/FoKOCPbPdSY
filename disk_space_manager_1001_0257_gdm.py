# 代码生成时间: 2025-10-01 02:57:20
import os
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import ServerError, NotFound
import psutil


# 创建Sanic应用
app = Sanic('DiskSpaceManager')

# 获取磁盘使用情况的函数
def get_disk_usage(path):
    """
    获取指定路径的磁盘使用情况。
    :param path: 磁盘路径
    :return: 磁盘使用情况字典
    """
    try:
        usage = psutil.disk_usage(path)
        return {
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        }
    except Exception as e:
        # 异常处理，返回错误信息
        return {'error': str(e)}

# 定义Sanic路由
@app.route('/disk_usage', methods=['GET'])
async def disk_usage(request):
    """
    返回磁盘使用情况的API端点。
    :param request: 请求对象
    :return: JSON响应
    """
    path = request.args.get('path', default='/')
    try:
        disk_usage_info = get_disk_usage(path)
        return response.json(disk_usage_info)
    except ServerError as e:
        # 服务器错误处理
        return response.json({'error': str(e)}, status=500)
    except NotFound as e:
        # 路径未找到错误处理
        return response.json({'error': str(e)}, status=404)
    except Exception as e:
        # 其他异常处理
        return response.json({'error': str(e)}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)