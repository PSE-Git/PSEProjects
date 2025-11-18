"""Check actual ClientDetails table schema"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Connection details
host = "34.100.231.86"
port = 3306
user = "Karthiga"
password = "Pranu@25BK"
database = "PSEAutoProposal"

ssl_config = {
    'ca': 'certs/server-ca.pem',
    'cert': 'certs/client-cert.pem',
    'key': 'certs/client-key.pem',
    'check_hostname': False
}

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl=ssl_config
    )
    
    cursor = conn.cursor()
    cursor.execute("DESCRIBE ClientDetails")
    
    print("ClientDetails Table Schema:")
    print("=" * 80)
    print(f"{'Field':<25} {'Type':<20} {'Null':<8} {'Key':<8} {'Default':<15} {'Extra'}")
    print("=" * 80)
    
    for row in cursor.fetchall():
        field, type_, null, key, default, extra = row
        print(f"{field:<25} {type_:<20} {null:<8} {key:<8} {str(default):<15} {extra}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
