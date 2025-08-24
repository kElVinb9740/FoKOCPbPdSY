# 代码生成时间: 2025-08-25 04:35:34
import yaml
from sanic import Sanic, response
from sanic.exceptions import ServerError, abort
from sanic.config import Config
from sanic.log import logger


# Define the application
app = Sanic("ConfigManager")
config = Config()

# Load configuration from a YAML file
def load_config(file_path: str):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        abort(404, 'Configuration file not found')
    except yaml.YAMLError as e:
        abort(500, 'Failed to parse configuration file')

# Initialize the configuration data
config_data = load_config('config.yaml')

# Define a route to retrieve the configuration
@app.route("/config", methods=["GET"])
async def get_config(request):
    """
    Retrieves the configuration data.
    
    :query int refresh: Force reload configuration file. Defaults to 0.
    :return: JSON response containing the configuration data.
    """
    refresh = request.args.get('refresh', type=int, default=0)
    if refresh == 1:
        config_data = load_config('config.yaml')
    return response.json(config_data)

# Define a route to update the configuration
@app.route("/config", methods=["POST"])
async def update_config(request):
    """
    Updates the configuration data.
    
    :json dict new_config: New configuration data.
    :return: JSON response containing the updated configuration data.
    """
    try:
        new_config = request.json
        with open('config.yaml', 'w') as file:
            yaml.dump(new_config, file, default_flow_style=False)
        global config_data
        config_data = new_config
        return response.json(config_data)
    except (yaml.YAMLError, TypeError) as e:
        abort(400, 'Failed to update configuration file')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)