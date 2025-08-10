# 代码生成时间: 2025-08-10 16:19:36
import psutil
from sanic import Sanic, response

# 定义Sanic应用
app = Sanic('SystemPerformanceMonitor')

# 监控系统CPU使用率的路由
@app.route('/cpu', methods=['GET'])
async def monitor_cpu(request):
    # 获取CPU使用率
    cpu_usage = psutil.cpu_percent(interval=1)
    # 返回CPU使用率
    return response.json({'cpu_usage': cpu_usage})

# 监控系统内存使用率的路由
@app.route('/memory', methods=['GET'])
async def monitor_memory(request):
    # 获取内存使用情况
    memory = psutil.virtual_memory()
    # 返回内存使用率
    return response.json({'memory_usage': memory.percent})

# 监控系统磁盘使用率的路由
@app.route('/disk', methods=['GET'])
async def monitor_disk(request):
    # 获取磁盘使用情况
    disk = psutil.disk_usage('/')
    # 返回磁盘使用率
    return response.json({'disk_usage': disk.percent})

# 错误处理中间件
@app.exception_handler(psutil.Error)
async def handle_psutil_error(request, exception):
    # 如果psutil发生错误，返回错误信息
    return response.json({'error': str(exception)}, status=500)

# 启动Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
