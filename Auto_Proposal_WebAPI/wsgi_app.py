"""
ASGI/WSGI wrapper for IIS deployment
This file wraps the FastAPI application for compatibility with wfastcgi
"""

import sys
import os

# Add the project directory to the path
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# Set environment variable to allow all hosts
os.environ.setdefault('FORWARDED_ALLOW_IPS', '*')

# Import the FastAPI app
from src.auto_proposal.api.main import app

# Use a2wsgi for better ASGI to WSGI conversion
try:
    from a2wsgi import ASGIMiddleware
    application = ASGIMiddleware(app)
except ImportError:
    # Fallback to asgiref if a2wsgi is not available
    from asgiref.wsgi import WsgiHandler
    application = WsgiHandler(app)

def get_wsgi_application():
    """
    The WSGI application for wfastcgi
    """
    return application

if __name__ == "__main__":
    # For local testing
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
