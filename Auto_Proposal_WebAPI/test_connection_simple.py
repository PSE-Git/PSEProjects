"""Simple database connection test"""
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text

load_dotenv()

# Get credentials from .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

print(f"Testing connection to {db_host}:{db_port}/{db_name} as user {db_user}")

# Build URL with encoded password
encoded_password = quote_plus(db_password)
DATABASE_URL = f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}:{db_port}/{db_name}"

# SSL configuration
connect_args = {
    'ssl': {
        'ca': 'certs/server-ca.pem',
        'cert': 'certs/client-cert.pem',
        'key': 'certs/client-key.pem',
        'check_hostname': False
    },
    'ssl_verify_cert': False,
    'ssl_verify_identity': False
}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        current_db = result.fetchone()[0]
        print(f"✅ Connected to database: {current_db}")
        
        result = conn.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        print(f"\nTables found:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Test querying UserDetails
        result = conn.execute(text("SELECT COUNT(*) FROM UserDetails"))
        count = result.fetchone()[0]
        print(f"\n✅ UserDetails table has {count} records")
        
        result = conn.execute(text("SELECT COUNT(*) FROM CompanyDetails"))
        count = result.fetchone()[0]
        print(f"✅ CompanyDetails table has {count} records")
    
    engine.dispose()
    print("\n🎉 Connection test successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
