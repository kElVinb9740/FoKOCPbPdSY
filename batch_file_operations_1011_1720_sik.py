# 代码生成时间: 2025-10-11 17:20:57
import os
import shutil
from sanic import Sanic, response
from sanic.exceptions import ServerError, NotFound
from sanic.request import Request
from sanic.response import json

def copy_files(source_dir, target_dir):
    """Copies files from source directory to target directory.

    Args:
    source_dir (str): Path to the source directory.
    target_dir (str): Path to the target directory.

    Returns:
    bool: True if copy is successful, False otherwise."""
    try:
        for filename in os.listdir(source_dir):
# 添加错误处理
            source_file = os.path.join(source_dir, filename)
            target_file = os.path.join(target_dir, filename)
            if os.path.isfile(source_file):
# 改进用户体验
                shutil.copy2(source_file, target_file)
        return True
    except OSError as e:
        print(f"Error: {e}")
        return False

def delete_files(directory):
    "