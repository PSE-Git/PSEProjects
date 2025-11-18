# IP Address Update Required for Google Cloud SQL

## Current Situation
Your IP address has changed:
- **Old IP**: 106.200.11.220 (previously authorized)
- **New IP**: 106.200.12.88 (needs to be authorized)

This is why you're getting connection timeouts to the database.

## Steps to Fix:

### Option 1: Update IP in Google Cloud Console (Quick Fix)

1. Go to Google Cloud Console:
   https://console.cloud.google.com/sql/instances

2. Select your instance: `psedb1`

3. Click on **Connections** tab

4. Under **Authorized Networks**, find the old IP `106.200.11.220`

5. Either:
   - **Edit** the existing entry and change it to `106.200.12.88`
   - **OR Delete** the old entry and **Add new** with:
     - Name: `PSE-Karthiga-Updated`
     - Network: `106.200.12.88`

6. Click **Save**

7. Wait 30 seconds for changes to apply

### Option 2: Allow Range (For Dynamic IP)

If your IP changes frequently, you can authorize a range:
- Network: `106.200.0.0/16` (allows entire range)

### Option 3: Use Cloud SQL Proxy (Best for Production)

Install and use Cloud SQL Proxy to avoid IP whitelisting:

```bash
# Download Cloud SQL Proxy
# Windows:
curl -o cloud_sql_proxy.exe https://dl.google.com/cloudsql/cloud_sql_proxy.x64.exe

# Start proxy
.\cloud_sql_proxy.exe -instances=alert-outlet-475913-f7:asia-south1:psedb1=tcp:3306

# Then connect to localhost:3306 instead of 34.100.231.86:3306
```

## After Updating IP:

Test the connection:
```bash
python test_connection_simple.py
```

Then restart the API server:
```bash
python run.py
```

## Verify Your Current IP Anytime:

```powershell
(Invoke-WebRequest -Uri "https://api.ipify.org?format=text" -UseBasicParsing).Content
```
