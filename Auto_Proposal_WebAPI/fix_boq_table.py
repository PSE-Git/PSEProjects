"""
Fix PseApBoqItems table to add AUTO_INCREMENT to SNo column
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
conn = pymysql.connect(
    host='34.100.231.86',
    user='Karthiga',
    password='Pranu@25BK',
    database='PSEAutoProposal',
    ssl={
        'ca': 'certs/server-ca.pem',
        'cert': 'certs/client-cert.pem',
        'key': 'certs/client-key.pem',
        'check_hostname': False
    }
)

try:
    cursor = conn.cursor()
    
    print("Checking current table structure...")
    cursor.execute("SHOW CREATE TABLE PseApBoqItems")
    result = cursor.fetchone()
    print(f"\nCurrent table:\n{result[1]}\n")
    
    print("Adding AUTO_INCREMENT to SNo column...")
    
    # Modify the SNo column to add AUTO_INCREMENT
    alter_sql = """
    ALTER TABLE PseApBoqItems 
    MODIFY COLUMN SNo INT NOT NULL AUTO_INCREMENT
    """
    
    cursor.execute(alter_sql)
    conn.commit()
    
    print("✅ Successfully added AUTO_INCREMENT to SNo column")
    
    # Verify the change
    cursor.execute("SHOW CREATE TABLE PseApBoqItems")
    result = cursor.fetchone()
    print(f"\nUpdated table:\n{result[1]}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    conn.close()

print("\nDone! You can now use the BOQ items API to create new items.")
