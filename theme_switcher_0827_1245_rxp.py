# 代码生成时间: 2025-08-27 12:45:15
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request

# 应用配置
class AppConfig:
    # 存储当前主题
    current_theme = 'light'

# 应用定义
app = Sanic('ThemeSwitcherApp')

# 路由：获取当前主题
@app.route('/api/theme', methods=['GET'])
async def get_theme(request: Request):
    # 返回当前主题
    return response.json({'theme': app.config.current_theme})

# 路由：切换主题
@app.route('/api/theme', methods=['POST'])
async def switch_theme(request: Request):
    try:
        # 获取请求体中的主题
        body = request.json
        if 'theme' not in body:
            raise ValueError('Theme not provided in the request body')

        # 验证主题
        if body['theme'] not in ['light', 'dark']:
            raise ValueError('Invalid theme value')

        # 更新主题并返回
        app.config.current_theme = body['theme']
        return response.json({'theme': app.config.current_theme})
    except ValueError as ve:
        # 错误处理：返回错误信息
        return response.json({'error': str(ve)}, status=400)

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)