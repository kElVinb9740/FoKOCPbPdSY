# 代码生成时间: 2025-09-10 11:04:43
import asyncio
from sanic import Sanic
from sanic.response import json, text, file
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

# 创建一个Sanic应用
app = Sanic('ExcelGenerator')

# 定义生成Excel文件的函数
async def generate_excel(request):
    # 创建一个工作簿
    wb = Workbook()
    # 激活默认工作表
    ws = wb.active
    # 为工作表命名
    ws.title = 'Generated Sheet'
    
    # 模拟数据
    data = {
        'Name': ['John', 'Jane', 'Alice'],
        'Age': [28, 22, 35],
        'City': ['New York', 'Los Angeles', 'Chicago']
    }
    
    # 将字典转换为DataFrame
    df = DataFrame(data)
    
    # 将DataFrame转换为工作表中的行
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    # 保存工作簿为Excel文件
    file_path = 'generated_excel.xlsx'
    wb.save(file_path)
    
    # 返回文件
    return file(file_path)

# 定义Sanic路由
@app.route('/generate_excel', methods=['GET'])
async def excel_handler(request):
    try:
        # 调用生成Excel的函数
        return await generate_excel(request)
    except Exception as e:
        # 错误处理，返回错误信息
        return json({'error': str(e)})

# 定义Sanic启动函数
def start_server():
    host = '127.0.0.1'
    port = 8000
    app.run(host=host, port=port, debug=True)

# 程序入口点
if __name__ == '__main__':
    start_server()

# 注意：
# 1. 需要安装openpyxl和pandas库
# 2. 可以通过Python的pip命令安装：pip install openpyxl pandas
# 3. 访问'http://127.0.0.1:8000/generate_excel'来触发Excel文件生成
