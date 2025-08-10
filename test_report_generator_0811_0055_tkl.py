# 代码生成时间: 2025-08-11 00:55:00
import os
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.exceptions import ServerError, ServerErrorMiddleware
from jinja2 import Environment, FileSystemLoader
import markdown2
import datetime

# 文件系统加载器路径
TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')

# 创建Sanic应用实例
app = Sanic('TestReportGenerator')

# 初始化Jinja2模板环境
env = Environment(loader=FileSystemLoader(TEMPLATE_FOLDER))
# 添加错误处理

# 确保模板文件夹存在
if not os.path.exists(TEMPLATE_FOLDER):
    os.makedirs(TEMPLATE_FOLDER)

# 测试报告模板
TEST_REPORT_TEMPLATE = env.get_template('test_report_template.html')

# 生成测试报告的路由
@app.route('/report', methods=['POST'])
async def generate_report(request: Request):
    try:
        # 从请求中获取测试结果数据
        test_results = request.json
        
        # 将测试结果转换为Markdown格式
        markdown_results = markdown2.markdown(str(test_results))
        
        # 将当前日期和时间添加到模板上下文中
        context = {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'results': markdown_results
        }
        
        # 使用模板生成测试报告
        report = TEST_REPORT_TEMPLATE.render(context)
        
        # 返回测试报告作为响应
# TODO: 优化性能
        return response.html(report)
    except Exception as e:
        # 错误处理
        return response.json({'error': str(e)}, status=500)

# 错误处理中间件
class ErrorHandler(ServerErrorMiddleware):
    async def server_error(self, request, exception):
        # 服务器内部错误处理
        return response.json({'error': 'Internal Server Error'}, status=500)

# 将错误处理中间件添加到Sanic应用中
app.register_error_handler(ServerError, ErrorHandler())

# 运行Sanic应用
# 改进用户体验
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

# 注意：
# - 请确保templates文件夹中存在test_report_template.html模板文件
# - 该模板文件应包含用于渲染测试结果的适当HTML结构
# - 此代码假设测试结果以JSON格式发送到/report端点
# 添加错误处理
# - 错误处理中间件捕获并返回所有服务器内部错误
# TODO: 优化性能
