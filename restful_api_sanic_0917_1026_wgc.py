# 代码生成时间: 2025-09-17 10:26:47
import sanic
from sanic.response import json, text
from sanic.exceptions import ServerError, ServerNotFoundError

"""
RESTful API using Sanic framework
"""

app = sanic.Sanic("RESTfulAPI")


@app.route("/", methods="GET")
async def root(request):
    """
    Root endpoint to test API connectivity
    """
    return text("API is up and running")


@app.route("/items/", methods="GET")
async def get_items(request):
    """
    GET endpoint to retrieve all items
    """
    # Simulated data
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"}
    ]
    return json(items)


@app.route("/items/<int:item_id>/", methods="GET")
async def get_item(request, item_id):
    """
    GET endpoint to retrieve a single item by ID
    """
    # Simulated data
    items = [
        {"id": 1, "name": "Item 1"},
        {"id": 2, "name": "Item 2"},
        {"id": 3, "name": "Item 3"}
    ]
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return json(item)
    else:
        return json({"error": "Item not found"}, status=404)


@app.route("/items/", methods="POST")
async def create_item(request):
    """
    POST endpoint to create a new item
    """
    try:
        item_data = request.json
        # Simulated data storage
        items.append(item_data)
        return json(item_data, status=201)
    except Exception as e:
        raise ServerError(f"Failed to create item: {e}")


@app.exception(ServerNotFoundError)
async def server_not_found_exception(request, exception):
    """
    Handle 404 errors
    """
    return json({"error": "Resource not found"}, status=404)


@app.exception(ServerError)
async def server_error_exception(request, exception):
    """
    Handle internal server errors
    """
    return json({"error": str(exception)}, status=500)


if __name__ == "__main__":
    """
    Run the Sanic server
    """
    app.run(host="0.0.0.0", port=8000, debug=True)