"""Test importing the app to see any errors"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

try:
    print("Attempting to import app...")
    from src.auto_proposal.api.main import app
    print("✓ App imported successfully!")
    print(f"✓ Routes registered: {[route.path for route in app.routes]}")
except Exception as e:
    print(f"✗ Error importing app: {str(e)}")
    import traceback
    traceback.print_exc()
