# IIS Deployment Guide - Auto Proposal WebAPI

This guide provides complete instructions for deploying the Auto Proposal WebAPI to Internet Information Services (IIS).

## Prerequisites

- Windows Server 2016 or later / Windows 10/11 Pro
- IIS installed with CGI support
- Python 3.9 or higher installed
- Admin privileges on the server

## Quick Deployment

Run the automated deployment script:

```powershell
.\deploy_to_iis.ps1
```

This script will:
1. Check Python installation
2. Install required packages (wfastcgi, asgiref)
3. Enable wfastcgi in IIS
4. Update web.config with correct paths
5. Create necessary directories
6. Test the application

## Manual Deployment Steps

### 1. Install IIS with CGI Support

```powershell
# Run as Administrator
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole
Enable-WindowsOptionalFeature -Online -FeatureName IIS-CGI
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIExtensions
Enable-WindowsOptionalFeature -Online -FeatureName IIS-ISAPIFilter
```

### 2. Install Python Packages

```powershell
pip install -r requirements.txt
pip install wfastcgi asgiref
```

### 3. Enable wfastcgi

```powershell
wfastcgi-enable
```

Note the output - it shows the script processor path you'll need.

### 4. Configure IIS

#### 4.1 Create Application Pool

1. Open IIS Manager (`inetmgr`)
2. Right-click "Application Pools" → "Add Application Pool"
   - Name: `AutoProposalAPI`
   - .NET CLR version: `No Managed Code`
   - Managed pipeline mode: `Integrated`
3. Click OK

#### 4.2 Configure Application Pool Settings

1. Select the `AutoProposalAPI` pool
2. Click "Advanced Settings"
   - Enable 32-Bit Applications: `False`
   - Start Mode: `AlwaysRunning`
   - Idle Time-out: `0` (or higher value)
3. Click OK

#### 4.3 Create Website

1. Right-click "Sites" → "Add Website"
   - Site name: `AutoProposalAPI`
   - Application pool: `AutoProposalAPI`
   - Physical path: `D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI`
   - Binding:
     - Type: `http`
     - IP address: `All Unassigned`
     - Port: `8000`
     - Host name: (leave empty or add your domain)
2. Click OK

### 5. Set Folder Permissions

The IIS application pool needs access to your project folder:

```powershell
# Run as Administrator
$projectPath = "D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI"
$acl = Get-Acl $projectPath
$permission = "IIS AppPool\AutoProposalAPI", "Modify", "ContainerInherit,ObjectInherit", "None", "Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl $projectPath $acl
```

Or manually:
1. Right-click project folder → Properties → Security
2. Click Edit → Add
3. Type `IIS AppPool\AutoProposalAPI`
4. Click "Check Names" → OK
5. Grant "Modify" permissions
6. Apply changes

### 6. Configure Handler Mapping (if needed)

If not auto-configured via web.config:

1. In IIS Manager, select your site
2. Double-click "Handler Mappings"
3. Click "Add Module Mapping"
   - Request path: `*`
   - Module: `FastCgiModule`
   - Executable: `C:\Python311\python.exe|C:\Python311\Lib\site-packages\wfastcgi.py`
   - Name: `PythonHandler`
4. Click OK

### 7. Update web.config

The `web.config` file should have correct paths. Update if needed:

- `scriptProcessor`: Your Python path and wfastcgi.py path
- `PYTHONPATH`: Your project directory
- `WSGI_LOG`: Path for logs

### 8. Test the Deployment

1. Start the website in IIS Manager
2. Open browser: `http://localhost:8000/docs`
3. You should see the FastAPI Swagger documentation

## Environment Variables

Create a `.env` file in the project root (if not exists):

```env
# Database Configuration
DB_HOST=34.100.231.86
DB_PORT=3306
DB_USER=Karthiga
DB_PASSWORD=Pranu@25BK
DB_NAME=PSEAutoProposal

# SSL Configuration
SSL_CA=./certs/server-ca.pem
SSL_CERT=./certs/client-cert.pem
SSL_KEY=./certs/client-key.pem

# Cloud SQL Connector
USE_CLOUD_SQL_CONNECTOR=false
```

## Troubleshooting

### Issue: 500 Internal Server Error

**Solutions:**
1. Check IIS error logs: `C:\inetpub\logs\LogFiles`
2. Check wfastcgi logs: `D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI\logs\wfastcgi.log`
3. Enable detailed errors in web.config (already set)
4. Verify Python path in web.config matches your installation

### Issue: Module not found errors

**Solution:**
Ensure all packages are installed in the same Python environment that IIS uses:

```powershell
python -m pip list
python -c "import fastapi; import sqlalchemy; import pymysql; print('All imports successful')"
```

### Issue: Database connection fails

**Solutions:**
1. Verify your current IP is authorized in Google Cloud SQL
2. Check IP using: `Invoke-RestMethod "https://api.ipify.org?format=json"`
3. Add IP to Google Cloud SQL authorized networks
4. Verify SSL certificates exist in `./certs/` folder

### Issue: Permission denied errors

**Solution:**
Grant IIS AppPool user full permissions:

```powershell
icacls "D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI" /grant "IIS AppPool\AutoProposalAPI:(OI)(CI)F" /T
```

### Issue: Application Pool stops

**Solutions:**
1. Check Windows Event Viewer → Application logs
2. Increase Idle Time-out in Application Pool settings
3. Set "Start Mode" to "AlwaysRunning"
4. Check for Python errors in the application code

## Performance Optimization

### 1. Enable Output Caching

In IIS Manager:
1. Select your site
2. Double-click "Output Caching"
3. Add caching rules for static content

### 2. Enable Compression

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionDynamic
Enable-WindowsOptionalFeature -Online -FeatureName IIS-HttpCompressionStatic
```

### 3. Configure Application Pool Recycling

1. Select Application Pool → Advanced Settings
2. Configure:
   - Regular Time Interval: `1740` (29 hours)
   - Specific Times: Add off-peak hours

## Security Considerations

### 1. SSL/TLS Configuration

For production, configure HTTPS:

1. Obtain SSL certificate
2. In IIS Manager → Site Bindings
3. Add https binding with certificate
4. Update API base URL

### 2. Request Filtering

Configure request size limits in web.config:

```xml
<system.webServer>
  <security>
    <requestFiltering>
      <requestLimits maxAllowedContentLength="52428800" /> <!-- 50 MB -->
    </requestFiltering>
  </security>
</system.webServer>
```

### 3. Authentication

For production, enable Windows Authentication or configure API key authentication in the FastAPI application.

## Monitoring

### Check Application Status

```powershell
# Check if site is running
Get-Website -Name "AutoProposalAPI"

# Check application pool status
Get-WebAppPoolState -Name "AutoProposalAPI"

# View recent logs
Get-Content "D:\PSE\Projects\Auto\Coding\Auto_Proposal_WebAPI\logs\wfastcgi.log" -Tail 50
```

### Health Check Endpoint

Access: `http://localhost:8000/docs` to verify API is running

## Updating the Application

When you update code:

```powershell
# Stop the application pool
Stop-WebAppPool -Name "AutoProposalAPI"

# Update your code (git pull, copy files, etc.)

# Start the application pool
Start-WebAppPool -Name "AutoProposalAPI"
```

Or simply restart IIS:

```powershell
iisreset
```

## Alternative: Using Reverse Proxy

Instead of wfastcgi, you can use IIS as a reverse proxy to Uvicorn:

1. Install URL Rewrite and ARR (Application Request Routing)
2. Keep Uvicorn running as a Windows Service
3. Configure IIS to proxy requests to `http://localhost:8000`

This approach is often more performant for ASGI applications.

## Production Checklist

- [ ] SSL certificate configured
- [ ] Database credentials secured (environment variables or Azure Key Vault)
- [ ] Error logging configured
- [ ] Backup strategy implemented
- [ ] Monitoring and alerts set up
- [ ] Security headers configured
- [ ] CORS policies reviewed
- [ ] Rate limiting implemented
- [ ] IP whitelisting configured in Google Cloud SQL
- [ ] Application pool configured for optimal performance
- [ ] Windows Firewall rules configured

## Support

For issues specific to:
- **FastAPI**: https://fastapi.tiangolo.com/
- **IIS**: https://www.iis.net/
- **wfastcgi**: https://pypi.org/project/wfastcgi/

## Additional Resources

- [FastAPI Deployment Documentation](https://fastapi.tiangolo.com/deployment/)
- [IIS Configuration Reference](https://docs.microsoft.com/en-us/iis/configuration/)
- [Python on IIS](https://docs.microsoft.com/en-us/visualstudio/python/configure-web-apps-for-iis-windows)
