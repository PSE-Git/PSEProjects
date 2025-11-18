from setuptools import setup, find_packages

setup(
    name="auto_proposal",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.4.2",
        "python-dotenv==1.0.0",
        "reportlab==4.0.7",
        "pytest==7.4.3",
        "httpx==0.25.1",
        "python-multipart==0.0.6",
        "pymysql==1.1.0",
        "psycopg2-binary==2.9.9",
        "python-jose==3.3.0",
        "pandas==2.1.2"
    ],
)