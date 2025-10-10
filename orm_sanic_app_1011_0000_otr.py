# 代码生成时间: 2025-10-11 00:00:21
import asyncio
from sanic import Sanic
from sanic.response import json
from peewee import Model, SqliteDatabase, Field

# ORM 框架配置
db = SqliteDatabase('app.db')

# 定义 ORM 模型类
class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = Field(primary_key=True)
    username = Field(unique=True)
    email = Field(unique=True)
    password = Field()

# 初始化数据库
async def init_db():
    await db.create_tables([User], safe=True)

# Sanic 应用配置
app = Sanic('ORM_Sanic_App')

# REST API 路由：创建用户
@app.route('/users', methods=['POST'])
async def create_user(request):
    data = request.json
    try:
        user = User.create(username=data['username'], email=data['email'], password=data['password'])
        return json({'message': 'User created successfully', 'user': user.username}, status=201)
    except Exception as e:
        return json({'error': str(e)}, status=400)

# REST API 路由：获取所有用户
@app.route('/users', methods=['GET'])
async def get_users(request):
    try:
        users = User.select()
        return json([{'username': user.username, 'email': user.email} for user in users])
    except Exception as e:
        return json({'error': str(e)}, status=500)

# Sanic 应用启动
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    app.run(host='0.0.0.0', port=8000, auto_reload=False)