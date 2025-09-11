# 代码生成时间: 2025-09-11 15:03:11
import random
from sanic import Sanic, response


# 创建Sanic应用
app = Sanic("RandomNumberGenerator")


@app.route("/generate", methods="POST")
async def generate_random_number(request):
    # 解析请求体
    data = request.json
    # 检查请求数据是否包含必要的参数
    if "min" not in data or "max" not in data:
        return response.json(
            {
                "error": "Missing parameters in request. Both 'min' and 'max' are required."
            },
            status=400
        )
    
    # 检查参数类型
    try:
        min_val = int(data["min"])
        max_val = int(data["max"])
    except ValueError:
        return response.json(
            {
                "error": "Invalid input type. 'min' and 'max' should be integers."
            },
            status=400
        )
    
    # 生成随机数
    random_number = random.randint(min_val, max_val)
    # 返回随机数
    return response.json(
        {
            "random_number": random_number
        }
    )


if __name__ == "__main__":
    # 运行Sanic应用
    app.run(host="0.0.0.0", port=8000)