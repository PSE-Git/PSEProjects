"""
Direct password test without URL encoding
"""
import pymysql
import os

# Test connection with raw password
try:
    print("Testing direct connection with password: Pranu@25BK")
    
    ssl_config = {
        'ca': 'certs/server-ca.pem',
        'cert': 'certs/client-cert.pem',
        'key': 'certs/client-key.pem',
        'check_hostname': False
    }
    
    connection = pymysql.connect(
        host='34.100.231.86',
        user='Karthiga',
        password='Pranu@25BK',
        database='PSEAutoProposal',
        port=3306,
        ssl=ssl_config,
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )
    
    print("✅ Connection successful!")
    
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE()")
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"\nTables in database:")
    for table in tables:
        print(f"  - {table[0]}")
    
    connection.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
