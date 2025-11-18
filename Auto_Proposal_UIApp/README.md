# Auto Proposal UI (Flask + Tailwind)

Lightweight server-rendered frontend for the Auto-Proposal system.

This project is a Flask + Jinja2 web UI that uses TailwindCSS via CDN for styling. The frontend is deployed separately from the backend webservice.

Prerequisites
- Python 3.8+
- (Recommended) a virtual environment

Quick start (PowerShell)

```powershell
# from project root
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Copy your PSE logo into the project static folder (one-time):
# Copy from: d:\PSE\Logo\Logo.png
# To:       ./static/logo.png
# Example (PowerShell):
# If you already placed the logo at `image/logo.png` (project path), the app will serve it automatically.
# Example (PowerShell) to copy into the project image folder (if needed):
Copy-Item -Path "d:\PSE\Logo\Logo.png" -Destination .\image\logo.png

$env:FLASK_APP = 'app.py'; python -m flask run --host=127.0.0.1 --port=5000
```

Open http://127.0.0.1:5000 in your browser.

Notes
- Tailwind is loaded via CDN for simplicity and fast iteration. If you want a build pipeline (for production), add a Tailwind build step.
 - The UI uses a brown brand palette (to match the provided logo). The app will serve the logo found at `image/logo.png` inside the project.
