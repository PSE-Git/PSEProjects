"""
Test Google Cloud SQL MySQL Connection
Run this script to verify your database connection works.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in .env file")
        print("Please create a .env file with your database connection string.")
        return False
    
    # Hide password in output
    safe_url = DATABASE_URL.split('@')
    if len(safe_url) > 1:
        print(f"🔗 Attempting to connect to: {safe_url[1]}")
    else:
        print(f"🔗 Attempting to connect to database...")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()[0]
            print(f"✅ Connection successful!")
            print(f"📊 MySQL Version: {version}")
            
            # Test database selection
            result = conn.execute(text("SELECT DATABASE()"))
            current_db = result.fetchone()[0]
            print(f"📁 Current Database: {current_db}")
            
            # List tables
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            if tables:
                print(f"📋 Existing tables: {[table[0] for table in tables]}")
            else:
                print("📋 No tables found (database is empty)")
            
        engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed!")
        print(f"Error: {str(e)}")
        print("\nCommon issues:")
        print("1. Check if your IP is authorized in Google Cloud Console")
        print("2. Verify username and password are correct")
        print("3. Ensure the database exists")
        print("4. Check if the instance is running")
        return False

def create_database_if_needed():
    """Create database if it doesn't exist."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # Parse URL to get database name
    try:
        db_name = DATABASE_URL.split('/')[-1].split('?')[0]
        print(f"\n📝 Database name from URL: {db_name}")
        
        # Connect without specifying database
        base_url = '/'.join(DATABASE_URL.split('/')[:-1])
        engine = create_engine(base_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            if not result.fetchone():
                print(f"Creating database: {db_name}")
                conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
                conn.commit()
                print(f"✅ Database {db_name} created successfully!")
            else:
                print(f"✅ Database {db_name} already exists")
        
        engine.dispose()
        
    except Exception as e:
        print(f"⚠️ Could not create database: {str(e)}")
        print("You may need to create it manually in Google Cloud Console or MySQL client")

if __name__ == "__main__":
    print("=" * 60)
    print("Google Cloud SQL MySQL Connection Test")
    print("=" * 60)
    
    if test_connection():
        print("\n" + "=" * 60)
        print("✅ Your database connection is working correctly!")
        print("=" * 60)
        
        # Ask if they want to initialize tables
        print("\nNext steps:")
        print("1. Run: python -c 'from src.auto_proposal.db.database import init_db; init_db()'")
        print("   This will create all necessary tables")
        print("2. Run: python run.py")
        print("   This will start your API server")
    else:
        print("\n" + "=" * 60)
        print("❌ Please fix the connection issues and try again")
        print("=" * 60)
        print("\nRefer to GOOGLE_CLOUD_SETUP.md for detailed setup instructions")
