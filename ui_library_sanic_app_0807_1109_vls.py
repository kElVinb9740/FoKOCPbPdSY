# 代码生成时间: 2025-08-07 11:09:33
from sanic import Sanic, response
from sanic.exceptions import ServerError, ServerNotInitialized
from sanic.response import json
from jinja2 import FileSystemLoader, Environment

# Initialize the Sanic application
app = Sanic("UI Library")

# Define templates directory
TEMPLATES_DIR = "./templates"
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Define a route to return a list of UI components
@app.route("/components", methods=["GET"])
async def get_components(request):
    # Simulate fetching components from a database or another source
    components = [
        "Button",
        "Input",
        "Label",
        "Checkbox",
        "Radio",
        "Select",
        "ButtonGroup"
    ]
    try:
        # Return the components in JSON format
        return response.json(components)
    except Exception as e:
        # Handle any exceptions and return a JSON error response
        return response.json(
            {"error": "An error occurred while fetching components"}, status=500
        )

# Define a route to render a template for a specific UI component
@app.route("/component/<component_name>", methods=["GET"])
async def render_component(request, component_name):
    try:
        # Render the template for the requested component
        template = env.get_template(f"{component_name}.html")
        component_html = template.render()
        return response.html(component_html)
    except Exception as e:
        # Handle any exceptions and return a JSON error response
        return response.json(
            {"error": f"Component {component_name} not found"}, status=404
        )

# Run the application
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8000, debug=True)
    except ServerNotInitialized:
        app.init()
        app.run(host="0.0.0.0", port=8000, debug=True)
    except ServerError as e:
        print(f"Server error occurred: {e}")
