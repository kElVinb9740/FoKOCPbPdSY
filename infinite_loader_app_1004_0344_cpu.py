# 代码生成时间: 2025-10-04 03:44:21
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerErrorMiddleware


# 定义全局变量，用于控制加载行为
infinite_load_active = True


# 定义一个简单的服务，用于处理无限加载请求
app = Sanic('InfiniteLoaderApp')


# 无限加载的路由
@app.route('/load-more', methods=['GET'])
async def load_more(request):
    """
    处理客户端的无限加载请求。
    如果全局变量infinite_load_active为True，则返回新的数据，否则返回结束加载的信号。
    """
    global infinite_load_active
    
    try:
        if infinite_load_active:
            # 模拟数据加载
            data = {'id': 1, 'message': 'New item loaded'}
            return response.json({'status': 'success', 'data': data})
        else:
            # 结束加载
            return response.json({'status': 'end', 'message': 'No more items to load'})
    except Exception as e:
        # 错误处理
        return response.json({'status': 'error', 'message': str(e)})


# 停止无限加载的路由
@app.route('/stop-loading', methods=['POST'])
async def stop_loading(request):
    """
    处理停止无限加载的请求。
    设置全局变量infinite_load_active为False，停止数据加载。
    """
    global infinite_load_active
    try:
        infinite_load_active = False
        return response.json({'status': 'success', 'message': 'Loading stopped'})
    except Exception as e:
        # 错误处理
        return response.json({'status': 'error', 'message': str(e)})


# 运行服务器
if __name__ == '__main__':
    # 运行Sanic应用
    app.run(host='0.0.0.0', port=8000, debug=True)
