# 代码生成时间: 2025-08-21 10:00:29
import psutil
import sanic
from sanic.response import json
from sanic.exceptions import ServerError, NotFound

# MemoryUsageAnalyzer class
class MemoryUsageAnalyzer:
    def __init__(self):
        pass

    def get_memory_usage(self):
        """Returns the current system memory usage in percentages."""
        mem = psutil.virtual_memory()
        return mem.percent

    def get_memory_stats(self):
        """Returns detailed memory statistics."""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }

# Sanic app
app = sanic.Sanic("MemoryUsageAnalyzer")

# Route to get the memory usage
@app.route("/memory_usage", methods=["GET"])
async def memory_usage(request):
    analyzer = MemoryUsageAnalyzer()
    try:
        usage = analyzer.get_memory_usage()
        return json({"memory_usage": usage})
    except Exception as e:
        raise ServerError("Failed to retrieve memory usage", e)

# Route to get the detailed memory statistics
@app.route("/memory_stats", methods=["GET"])
async def memory_stats(request):
    analyzer = MemoryUsageAnalyzer()
    try:
        stats = analyzer.get_memory_stats()
        return json(stats)
    except Exception as e:
        raise ServerError("Failed to retrieve memory statistics", e)

# Error handler for 404 Not Found
@app.exception(NotFound)
async def not_found_exception_handler(request, exception):
    return json({"error": "Resource not found"}, status=404)

# Error handler for ServerError
@app.exception(ServerError)
async def server_error_exception_handler(request, exception):
    return json({"error": exception.message}, status=500)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)