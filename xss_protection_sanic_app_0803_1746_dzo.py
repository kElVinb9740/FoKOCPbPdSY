# 代码生成时间: 2025-08-03 17:46:57
import html
import sanic
from sanic.response import html, json
from sanic import Blueprint

# 定义一个蓝图来组织路由
xss_protection_bp = Blueprint('xss_protection')

@xss_protection_bp.route("/", methods=["GET"])
async def home(request):
    # 显示主页，包含一个简单的表单
    return html("""
    <html>
    <head><title>XSS Protection</title></head>
    <body>
    <form action="/submit" method="post">
    <label for="user_input">Enter Text:</label><br>
    <input type="text" id="user_input" name="user_input"><br>
    <input type="submit" value="Submit">
    </form>
    </body>
    </html>
    """)

@xss_protection_bp.route("/submit", methods=["POST"])
async def submit(request):
    # 从表单中获取用户输入
    user_input = request.form.get("user_input")
    # 检查并清洗输入以防止XSS攻击
    if not user_input:
        return json({
            "error": "No input provided."
        }, status=400)

    # 使用html模块转义文本，防止XSS攻击
    sanitized_input = html.escape(user_input)

    # 将转义后的输入返回给用户
    return html("""
    <html>
    <head><title>Submitted Input</title></head>
    <body>
    <p>You entered: {}</p>
    </body>
    </html>
    """.format(sanitized_input))

# 创建Sanic应用并注册蓝图
app = sanic.Sanic("XSSProtectionApp")
app.blueprint(xss_protection_bp)

if __name__ == '__main__':
    # 运行应用
    app.run(host="0.0.0.0", port=8000, debug=True)
