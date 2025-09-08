# 代码生成时间: 2025-09-08 23:50:19
import math
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json
from sanic.exceptions import ServerError, InvalidUsage, abort

# Define the Sanic app
app = Sanic("MathCalculatorService")

# Define the endpoints for the math calculator service
@app.route("/add", methods=["GET"])
async def add(request: Request):
    """
    Handles the addition operation.
    :param request: The Sanic request object.
    :return: A JSON response with the result of the addition.
    """
    try:
        a = float(request.args.get("a", "0"))
        b = float(request.args.get("b", "0"))
        result = a + b
        return response.json({"result": result})
    except ValueError:
        # Handle the case where the input is not a number
        abort(400, "Invalid input for addition")


@app.route("/subtract", methods=["GET"])
async def subtract(request: Request):
    """
    Handles the subtraction operation.
    :param request: The Sanic request object.
    :return: A JSON response with the result of the subtraction.
    """
    try:
        a = float(request.args.get("a", "0"))
        b = float(request.args.get("b", "0"))
        result = a - b
        return response.json({"result": result})
    except ValueError:
        # Handle the case where the input is not a number
        abort(400, "Invalid input for subtraction")


@app.route("/multiply", methods=["GET"])
async def multiply(request: Request):
    """
    Handles the multiplication operation.
    :param request: The Sanic request object.
    :return: A JSON response with the result of the multiplication.
    """
    try:
        a = float(request.args.get("a", "0"))
        b = float(request.args.get("b", "0"))
        result = a * b
        return response.json({"result": result})
    except ValueError:
        # Handle the case where the input is not a number
        abort(400, "Invalid input for multiplication")


@app.route("/divide", methods=["GET"])
async def divide(request: Request):
    """
    Handles the division operation.
    :param request: The Sanic request object.
    :return: A JSON response with the result of the division.
    """
    try:
        a = float(request.args.get("a", "0"))
        b = float(request.args.get("b", "0"))
        if b == 0:
            abort(400, "Division by zero")
        result = a / b
        return response.json({"result": result})
    except ValueError:
        # Handle the case where the input is not a number
        abort(400, "Invalid input for division")


@app.route("/sqrt", methods=["GET"])
async def sqrt(request: Request):
    """
    Handles the square root operation.
    :param request: The Sanic request object.
    :return: A JSON response with the result of the square root.
    """
    try:
        number = float(request.args.get("number", "0"))
        if number < 0:
            abort(400, "Cannot take square root of negative number")
        result = math.sqrt(number)
        return response.json({"result": result})
    except ValueError:
        # Handle the case where the input is not a number
        abort(400, "Invalid input for square root")


# Run the Sanic app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)