# 代码生成时间: 2025-09-04 01:34:02
import base64
import os
from cryptography.fernet import Fernet


# 生成密钥并保存
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    return key

# 从文件中加载密钥
def load_key():
    return open('secret.key', 'rb').read()

# 加密函数
def encrypt_message(message, key):
    try:
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode())
        return encrypted_message.decode()
    except Exception as e:
        print(f"Encryption error: {e}")

# 解密函数
def decrypt_message(encrypted_message, key):
    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message.encode())
        return decrypted_message.decode()
    except Exception as e:
        print(f"Decryption error: {e}")

# Sanic 应用
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

app = Sanic('password_encryption_decryption')

# 加密路由
@app.route('/encrypt', methods=['POST'])
async def encrypt_request(request: Request):
    key = load_key()
    message = request.json.get('message')
    if not message:
        return response.json({'error': 'No message provided'}, status=400)
    encrypted_message = encrypt_message(message, key)
    return response.json({'encrypted_message': encrypted_message})

# 解密路由
@app.route('/decrypt', methods=['POST'])
async def decrypt_request(request: Request):
    key = load_key()
    encrypted_message = request.json.get('encrypted_message')
    if not encrypted_message:
        return response.json({'error': 'No encrypted message provided'}, status=400)
    decrypted_message = decrypt_message(encrypted_message, key)
    return response.json({'decrypted_message': decrypted_message})

# 确保密钥已经生成
if not os.path.exists('secret.key'):
    generate_key()
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
