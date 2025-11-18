"""Check current IP and database connection"""
import requests
import pymysql

# Get current public IP
try:
    response = requests.get("https://api.ipify.org?format=json")
    current_ip = response.json()["ip"]
    print(f"Current Public IP: {current_ip}")
    
    # Check if in authorized subnet 106.200.0.0/16
    ip_parts = current_ip.split('.')
    if ip_parts[0] == '106' and ip_parts[1] == '200':
        print("✓ IP is within authorized subnet 106.200.0.0/16")
    else:
        print(f"✗ IP {current_ip} is NOT in authorized subnet 106.200.0.0/16")
        print("  Your IP may not be authorized in Google Cloud SQL")
        
except Exception as e:
    print(f"Error getting IP: {e}")

print("\n" + "=" * 60)
print("Testing Database Connection...")
print("=" * 60)

ssl_config = {
    'ca': 'certs/server-ca.pem',
    'cert': 'certs/client-cert.pem',
    'key': 'certs/client-key.pem',
    'check_hostname': False
}

try:
    conn = pymysql.connect(
        host="34.100.231.86",
        port=3306,
        user="Karthiga",
        password="Pranu@25BK",
        database="PSEAutoProposal",
        ssl=ssl_config,
        connect_timeout=10
    )
    
    print("✓ Database connection successful!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ProposalItem WHERE ProposalId = 5")
    count = cursor.fetchone()[0]
    print(f"✓ Query successful! Found {count} items for Proposal ID 5")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"✗ Database connection failed!")
    print(f"Error: {e}")
    print("\nPossible issues:")
    print("1. Your IP is not authorized in Google Cloud SQL")
    print("2. Need to add your current IP to authorized networks")
    print(f"   Current IP: {current_ip}")
    print("   Authorized subnet: 106.200.0.0/16")
