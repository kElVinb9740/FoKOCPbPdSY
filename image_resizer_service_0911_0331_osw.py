# 代码生成时间: 2025-09-11 03:31:47
import os
from sanic import Sanic
from sanic.response import json, file
from PIL import Image
from io import BytesIO
import numpy as np
from typing import List

# Define the app
app = Sanic("ImageResizerService")

# Configuration for allowed image formats and the default size
ALLOWED_IMAGE_FORMATS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
DEFAULT_SIZE = (800, 600)

# Route to handle the file upload and resize
@app.route("/resize", methods=["POST"])
async def resize_images(request: Sanic.request):
    # Get the uploaded file from the request
    file = request.files.get('file')
    if not file:
        return json({'error': 'No file provided'}, status=400)

    # Check if the uploaded file is an image
    _, file_extension = os.path.splitext(file.filename)
    if file_extension.lower()[1:] not in ALLOWED_IMAGE_FORMATS:
        return json({'error': 'Unsupported file format'}, status=400)

    try:
        # Open the image file
        image = Image.open(file.file)
    except IOError:
        return json({'error': 'Failed to open the image file'}, status=500)

    try:
        # Calculate the new size based on the default size
        new_size = DEFAULT_SIZE
        image.thumbnail(new_size, Image.ANTIALIAS)

        # Save the resized image to a BytesIO object
        buffer = BytesIO()
        image.save(buffer, format=file_extension[1:])
        buffer.seek(0)
    except IOError:
        return json({'error': 'Failed to resize the image file'}, status=500)

    # Return the resized image as a response
    return file(buffer, filename=file.filename)

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

"""
    This service provides an endpoint '/resize' that accepts a POST request with a file upload.
    The file is expected to be an image (currently supporting png, jpg, jpeg, gif, bmp).
    Received images are resized to a default size (800x600) and returned as a file response.

    Error handling is included for cases where the file is not provided, the file format is unsupported,
    or the image cannot be opened or resized.

    The service is configured to run on port 8000 with debug mode enabled.
"""