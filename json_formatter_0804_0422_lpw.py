# 代码生成时间: 2025-08-04 04:22:00
import json
def convert_json(data, target_format):
    """Converts JSON data to different formats.

    Args:
        data (str): The JSON string to convert.
        target_format (str): The target format of the conversion (e.g., 'pretty', 'compact').

    Returns:
        str: The converted JSON string.

    Raises:
        ValueError: If the target format is not supported."""
    try:
        # Load the JSON data
        json_data = json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON data: " + str(e))
# 优化算法效率

    # Convert JSON data to the target format
    if target_format == 'pretty':
        return json.dumps(json_data, indent=4)
    elif target_format == 'compact':
        return json.dumps(json_data)
    else:
        raise ValueError("Unsupported target format: " + target_format)

# Sanic setup
from sanic import Sanic
from sanic.response import json as sanic_json

app = Sanic("JSON Formatter")

@app.route("/convert", methods=["POST"])
async def convert_json_request(request):
    "