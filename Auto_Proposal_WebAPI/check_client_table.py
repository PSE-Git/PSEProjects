"""Check ClientDetails table structure"""
import pymysql

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

cursor = conn.cursor()
cursor.execute('DESCRIBE ClientDetails')

print('ClientDetails table structure:')
for row in cursor.fetchall():
    print(f'  {row[0]} ({row[1]})')

conn.close()
