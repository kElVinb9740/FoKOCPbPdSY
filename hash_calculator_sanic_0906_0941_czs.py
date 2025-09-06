# 代码生成时间: 2025-09-06 09:41:58
import sanic
from sanic.response import json
import hashlib
def calculate_hash(data: str, algorithm: str = "sha256") -> str:
    """Calculates the hash of the given data using the specified algorithm.

    Args:
        data (str): The data to be hashed.
        algorithm (str): The hashing algorithm to use (default is 'sha256').

    Returns:
        str: The hash of the data in hexadecimal format.
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(data.encode('utf-8'))
        return hash_func.hexdigest()
    except AttributeError:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

app = sanic.Sanic("HashCalculator")

@app.route("/hash", methods=["POST"])
async def hash_endpoint(request: sanic.Request):
    """Handles POST requests to calculate the hash of the provided data.

    Args:
        request (sanic.Request): The incoming request.

    Returns:
        json: A JSON response containing the hash result.
    """
    try:
        data = request.json.get("data")
        algorithm = request.json.get("algorithm", "sha256")
        if data is None:
            return json({"error": "Missing data parameter"}, status=400)
        hash_result = calculate_hash(data, algorithm)
        return json({"hash": hash_result})
    except ValueError as e:
        return json({"error": str(e)}, status=400)
    except Exception as e:
        return json({"error": "Internal server error"}, status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)