# 代码生成时间: 2025-08-26 07:29:02
import asyncio
from sanic import Sanic
from sanic.response import json
from alembic.config import Config as AlembicConfig
from alembic import command
from sqlalchemy import create_engine

# Define the Sanic app
app = Sanic('DatabaseMigrationTool')

# Database configuration
DATABASE_URI = 'postgresql://user:password@localhost/dbname'  # Replace with actual database URI

# Initialize the Alembic configuration
def get_alembic_config():
    return AlembicConfig(
        "/path/to/your/alembic.ini"  # Replace with actual Alembic config path
    )

# Migrate the database up
@app.route('/migrate/up', methods=['POST'])
async def migrate_up(request):
    try:
        # Get the Alembic configuration
        alembic_cfg = get_alembic_config()
        
        # Migrate the database up
        command.upgrade(alembic_cfg, 'head')
        
        return json({'status': 'success', 'message': 'Migration successful'})
    except Exception as e:
        # Handle any migration errors
        return json({'status': 'error', 'message': str(e)})

# Migrate the database down
@app.route('/migrate/down', methods=['POST'])
async def migrate_down(request):
    try:
        # Get the Alembic configuration
        alembic_cfg = get_alembic_config()
        
        # Migrate the database down
        command.downgrade(alembic_cfg, '-1')
        
        return json({'status': 'success', 'message': 'Migration successful'})
    except Exception as e:
        # Handle any migration errors
        return json({'status': 'error', 'message': str(e)})

# Run the Sanic app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=1)
