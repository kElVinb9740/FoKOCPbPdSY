# 代码生成时间: 2025-08-17 10:06:29
import logging
from sanic import Sanic
from sanic.response import json
from sanic.log import logger

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

app = Sanic('ErrorLoggerService')

# 错误日志收集器路由
@app.route('/logs/collect', methods=['POST'])
async def collect_error_logs(request):
    """
    POST请求用于发送错误日志数据到服务端
    参数：
        - logs: 一个包含错误日志信息的列表
    响应：
        - 200: 成功接收日志
        - 400: 请求格式错误或缺少必要参数
    """
    try:
        # 尝试从请求体中获取日志数据
        logs = request.json.get('logs')
        if not logs:
            # 如果日志数据不存在，返回错误信息
            return json({'error': 'No logs provided'}, status=400)

        # 使用logging记录错误日志
        for log in logs:
            logger.error(log)

        return json({'message': 'Logs received successfully'}, status=200)
    except Exception as e:
        # 捕获任何异常并记录
        logger.error(f'Error collecting logs: {e}')
        return json({'error': 'Internal server error'}, status=500)

# 运行Sanic应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)