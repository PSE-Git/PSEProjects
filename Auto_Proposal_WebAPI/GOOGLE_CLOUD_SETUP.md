# Google Cloud SQL MySQL Setup Guide

## Connection Details
- **Instance Connection Name**: alert-outlet-475913-f7:asia-south1:psedb1
- **Public IP Address**: 34.100.231.86
- **Port**: 3306
- **Database Type**: MySQL

## Steps to Connect

### 1. Update .env File
Edit the `.env` file in the project root with your actual database credentials:

```env
DATABASE_URL=mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@34.100.231.86:3306/auto_proposal_db
```

Replace:
- `YOUR_USERNAME` - Your MySQL username (e.g., root or custom user)
- `YOUR_PASSWORD` - Your MySQL password
- `auto_proposal_db` - The database name you want to use

Example:
```env
DATABASE_URL=mysql+pymysql://admin:MySecurePass123@34.100.231.86:3306/auto_proposal_db
```

### 2. Configure Google Cloud SQL

#### Create Database
Connect to your Google Cloud SQL instance and create the database:

```sql
CREATE DATABASE auto_proposal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Create User (if needed)
```sql
CREATE USER 'appuser'@'%' IDENTIFIED BY 'YourSecurePassword';
GRANT ALL PRIVILEGES ON auto_proposal_db.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
```

#### Allow Your IP Address
1. Go to Google Cloud Console
2. Navigate to SQL > Instances > psedb1
3. Go to "Connections" tab
4. Under "Authorized networks", add your current IP address
5. Click "Save"

### 3. Install Required Python Package
Make sure PyMySQL is installed:

```powershell
pip install pymysql cryptography
```

### 4. Initialize the Database
Run this command to create all tables:

```powershell
python -c "from src.auto_proposal.db.database import init_db; init_db()"
```

Or use this script:

```powershell
cd src
python -c "from auto_proposal.db.database import init_db; init_db()"
```

### 5. Test the Connection
Create a simple test script:

```python
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to: {DATABASE_URL.split('@')[1]}")  # Hide credentials

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Database connection successful!")
except Exception as e:
    print(f"✗ Database connection failed: {str(e)}")
```

### 6. Run Your Application
```powershell
python run.py
```

### 7. Run Tests
The tests will still use SQLite in-memory database for speed and isolation.

```powershell
pytest tests/test_api.py -v
```

## Security Best Practices

1. **Use Strong Passwords**: Ensure your database password is strong
2. **Restrict IP Access**: Only allow necessary IP addresses in authorized networks
3. **Use SSL/TLS**: Consider enabling SSL for database connections
4. **Environment Variables**: Never commit .env file to version control
5. **Cloud SQL Proxy**: For production, consider using Cloud SQL Proxy for more secure connections

## Troubleshooting

### Connection Timeout
- Check if your IP is in the authorized networks
- Verify firewall rules allow port 3306

### Authentication Failed
- Double-check username and password
- Ensure user has proper permissions

### Database Not Found
- Create the database first using SQL command above
- Verify database name in connection string

### SSL Certificate Error
If you need SSL, update the connection string:
```env
DATABASE_URL=mysql+pymysql://user:pass@34.100.231.86:3306/auto_proposal_db?ssl_ca=/path/to/server-ca.pem&ssl_cert=/path/to/client-cert.pem&ssl_key=/path/to/client-key.pem
```

## Alternative: Using Cloud SQL Proxy

For better security, you can use Cloud SQL Proxy:

1. Download Cloud SQL Proxy
2. Run it:
   ```powershell
   ./cloud_sql_proxy -instances=alert-outlet-475913-f7:asia-south1:psedb1=tcp:3306
   ```
3. Update .env to use localhost:
   ```env
   DATABASE_URL=mysql+pymysql://user:pass@127.0.0.1:3306/auto_proposal_db
   ```

## Need Help?

If you encounter issues:
1. Check Google Cloud Console logs
2. Verify network connectivity: `Test-NetConnection -ComputerName 34.100.231.86 -Port 3306`
3. Check application logs
4. Review Google Cloud SQL documentation
