import pymysql
import bcrypt

# Connect to database
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
    },
    ssl_verify_cert=False,
    ssl_verify_identity=False
)

cur = conn.cursor()
cur.execute('SELECT UserID, Email, PasswordHash FROM UserDetails WHERE UserID=1')
result = cur.fetchone()

print(f"UserID: {result[0]}")
print(f"Email: {result[1]}")
print(f"PasswordHash: {result[2]}")
print(f"Hash is None: {result[2] is None}")

if result[2]:
    print(f"Hash length: {len(result[2])}")
    print(f"Hash starts with: {result[2][:10] if len(result[2]) >= 10 else result[2]}")
    
    # Test if it's a bcrypt hash
    if result[2].startswith('$2'):
        print("✓ Looks like a bcrypt hash")
    else:
        print("✗ Not a bcrypt hash - it's plain text!")
        print("The password stored is:", result[2])
        
        # Hash the plain password
        plain_password = result[2]
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(f"\nHashed version: {hashed}")
        
        # Update the database with hashed password
        cur.execute('UPDATE UserDetails SET PasswordHash = %s WHERE UserID = 1', (hashed,))
        conn.commit()
        print("✓ Password updated with bcrypt hash!")
else:
    print("Password is NULL in database")
    # Set the password
    hashed = bcrypt.hashpw('karthi1212'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cur.execute('UPDATE UserDetails SET PasswordHash = %s WHERE UserID = 1', (hashed,))
    conn.commit()
    print("✓ Password 'karthi1212' has been hashed and stored!")

conn.close()
print("\nDone!")
