# 代码生成时间: 2025-08-25 14:32:05
import os
import shutil
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import json

# Define the application
app = Sanic("FolderOrganizer")

# Define the API endpoint for organizing folders
@app.route("/organize", methods=["POST"])
async def organize_folders(request: Request):
    # Extract the target directory path from the request body
    try:
        target_dir = request.json.get("target_directory")
        if not target_dir:
            return response.json({"error": "Target directory not provided"}, status=400)
    except ValueError:
        return response.json({"error": "Invalid JSON in request"}, status=400)

    # Check if the target directory exists
    if not os.path.exists(target_dir):
        return response.json({"error": "Target directory does not exist"}, status=404)

    # Define the structure of the desired folder organization
    structure = {
        "Documents": [".docx", ".pdf", ".txt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Videos": [".mp4", ".avi", ".mov"],
        "Audio": [".mp3", ".wav", ".ogg"]
    }

    # Organize the files into the desired structure
    try:
        for folder_name, extensions in structure.items():
            folder_path = os.path.join(target_dir, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move files to the corresponding folders
            for file_name in os.listdir(target_dir):
                if any(file_name.endswith(ext) for ext in extensions):
                    source_path = os.path.join(target_dir, file_name)
                    destination_path = os.path.join(folder_path, file_name)
                    shutil.move(source_path, destination_path)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)

    return response.json({"message": "Folder organization completed"})

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)