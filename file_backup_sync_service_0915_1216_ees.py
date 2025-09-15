# 代码生成时间: 2025-09-15 12:16:03
import os
import shutil
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json

# 定义一些可能需要使用的常量
SUPPORTED_EXTENSIONS = {'txt', 'csv', 'doc', 'docx', 'pdf', 'xlsx', 'jpg'}

# 创建Sanic应用
app = Sanic("FileBackupSyncService")

# 错误处理函数
@app.exception(ServerError)
async def handle_server_error(request: Request, exception: Exception):
    return json({
        "error": True,
        "message": str(exception)
    }, status=500)

# 文件备份和同步的业务逻辑
def backup_and_sync_files(source_path: str, destination_path: str):
    """备份和同步文件到指定目录

    Args:
    source_path (str): 源文件夹路径
    destination_path (str): 目标文件夹路径

    Raises:
    FileNotFoundError: 如果源文件夹不存在
    PermissionError: 如果没有权限访问文件夹
    """
    try:
        # 检查源路径是否存在
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"源目录 {source_path} 不存在")

        # 检查目标路径是否存在，如果不存在则创建
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        # 遍历源目录中的文件
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            # 检查文件类型是否被支持
            if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in SUPPORTED_EXTENSIONS:
                destination_file_path = os.path.join(destination_path, filename)
                # 备份文件
                shutil.copy2(file_path, destination_file_path)

    except FileNotFoundError as e:
        raise FileNotFoundError(str(e))
    except PermissionError as e:
        raise PermissionError(str(e))
    except Exception as e:
        raise Exception(f"备份和同步文件时发生未知错误: {str(e)}")

# 定义API路由
@app.route("/backup-sync", methods=["POST"])
async def backup_sync(request: Request):
    """API端点：备份和同步文件"""
    # 获取请求体中的参数
    data = request.json
    source_path = data.get("source_path")
    destination_path = data.get("destination_path")

    # 参数验证
    if not source_path or not destination_path:
        return json({
            "error": True,
            "message": "源路径和目标路径必须提供"
        }, status=400)

    try:
        # 执行备份和同步操作
        backup_and_sync_files(source_path, destination_path)
        return json({
            "error": False,
            "message": "文件备份和同步成功"
        })
    except Exception as e:
        return json({
            "error": True,
            "message": str(e)
        }, status=500)

# 程序入口点
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)