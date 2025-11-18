from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Get database configuration from environment variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
use_cloud_connector = os.getenv("USE_CLOUD_SQL_CONNECTOR", "false").lower() == "true"
service_account_key = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Validate required credentials
if not all([db_user, db_password, db_name]):
    raise ValueError(
        "Database credentials missing! Required: DB_USER, DB_PASSWORD, DB_NAME"
    )

# Try to use Cloud SQL Connector if enabled and credentials available
if use_cloud_connector:
    try:
        from google.cloud.sql.connector import Connector
        
        db_instance_connection_name = os.getenv(
            "DB_INSTANCE_CONNECTION_NAME", 
            "alert-outlet-475913-f7:asia-south1:psedb1"
        )
        
        print(f"Connecting to Google Cloud SQL instance: {db_instance_connection_name}")
        print(f"Database: {db_name} as {db_user}")
        print("Using Cloud SQL Python Connector (no IP whitelisting required)")
        
        # Initialize Cloud SQL Python Connector
        connector = Connector()
        
        def getconn():
            """Create a database connection using Cloud SQL Connector."""
            return connector.connect(
                db_instance_connection_name,
                "pymysql",
                user=db_user,
                password=db_password,
                db=db_name
            )
        
        # Create SQLAlchemy engine using Cloud SQL Connector
        engine = create_engine(
            "mysql+pymysql://",
            creator=getconn,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        
    except Exception as e:
        print(f"⚠️  Cloud SQL Connector failed: {e}")
        print("Falling back to direct IP connection...")
        use_cloud_connector = False

# Direct IP connection (fallback or default)
if not use_cloud_connector:
    from urllib.parse import quote_plus
    
    db_host = os.getenv("DB_HOST", "34.100.231.86")
    db_port = os.getenv("DB_PORT", "3306")
    
    # URL encode the password
    encoded_password = quote_plus(db_password)
    
    # Build MySQL connection URL
    DATABASE_URL = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"
    
    print(f"Connecting to MySQL database: {db_host}:{db_port}/{db_name} as {db_user}")
    print("WARNING: Using direct IP connection - requires IP whitelisting in Google Cloud Console")
    print(f"Current connection will work only if your IP is authorized")
    
    # Get SSL certificate paths (optional for direct connection)
    ssl_ca = os.getenv("SSL_CA")
    ssl_cert = os.getenv("SSL_CERT")
    ssl_key = os.getenv("SSL_KEY")
    
    connect_args = {}
    if ssl_ca and ssl_cert and ssl_key:
        connect_args = {
            'ssl': {
                'ca': ssl_ca,
                'cert': ssl_cert,
                'key': ssl_key,
                'check_hostname': False
            },
            'ssl_verify_cert': False,
            'ssl_verify_identity': False
        }
        print(f"Using SSL certificates from: {ssl_ca}")
    
    # Create engine with direct connection
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=False
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables."""
    from ..core.models import Base
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()