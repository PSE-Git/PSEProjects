# Email and WhatsApp Setup Guide

## Issues Fixed

### 1. Email Not Sending
**Problem:** Email functionality requires SMTP credentials that weren't configured.

**Solution:** Set up environment variables for email configuration.

### 2. WhatsApp PDF Not Loading
**Problem:** WhatsApp was receiving a relative URL path (e.g., `/uploads/file.pdf`) instead of a full URL that can be accessed externally.

**Solution:** Updated to use absolute URL (e.g., `http://127.0.0.1:5000/uploads/file.pdf`).

---

## Email Configuration Setup

### Quick Setup (Recommended)

1. Run the setup script:
   ```powershell
   .\setup_email_config.ps1
   ```

2. Follow the prompts to enter:
   - Your email address
   - Your app password (see Gmail setup below)

3. Start your Flask app in the **same PowerShell window**:
   ```powershell
   python app.py
   ```

### Gmail Setup (Most Common)

1. **Enable 2-Factor Authentication:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Use the generated App Password** (NOT your regular Gmail password)

### Manual Environment Variable Setup

If you prefer to set variables manually:

```powershell
# For current session only
$env:SENDER_EMAIL = "youremail@gmail.com"
$env:SENDER_PASSWORD = "your-app-password-here"
$env:SMTP_SERVER = "smtp.gmail.com"
$env:SMTP_PORT = "587"
```

### Permanent Environment Variables (Optional)

To set permanently in Windows:

1. Open **System Properties** → **Environment Variables**
2. Add new **User variables**:
   - `SENDER_EMAIL` = your email
   - `SENDER_PASSWORD` = your app password
   - `SMTP_SERVER` = smtp.gmail.com
   - `SMTP_PORT` = 587

3. Restart your terminal/IDE

---

## Using Other Email Providers

### Outlook/Hotmail

```powershell
$env:SMTP_SERVER = "smtp-mail.outlook.com"
$env:SMTP_PORT = "587"
$env:SENDER_EMAIL = "youremail@outlook.com"
$env:SENDER_PASSWORD = "your-password"
```

### Yahoo Mail

```powershell
$env:SMTP_SERVER = "smtp.mail.yahoo.com"
$env:SMTP_PORT = "587"
$env:SENDER_EMAIL = "youremail@yahoo.com"
$env:SENDER_PASSWORD = "your-app-password"
```

---

## Testing Email Functionality

1. Ensure environment variables are set (run `setup_email_config.ps1` or set manually)

2. Start Flask app:
   ```powershell
   python app.py
   ```

3. Navigate to a proposal view page

4. Generate PDF

5. Click "Send Email" button

6. Check recipient's inbox

---

## WhatsApp PDF Sharing

**How it works now:**
- WhatsApp button creates a message with a **full URL** to the PDF
- The URL format is: `http://127.0.0.1:5000/uploads/filename.pdf`
- Recipient can click the link to download the PDF

**Important Notes:**
- ✅ Works when app is running on localhost (for testing)
- ❌ Will NOT work for external users (they can't access 127.0.0.1)

**For Production Use:**
You need to:
1. Deploy app to a public server with a domain name
2. Configure proper file hosting/CDN
3. Or upload PDFs to cloud storage (AWS S3, Google Cloud, etc.)

---

## Troubleshooting

### Email "Authentication Failed"
- Double-check your app password (not regular password)
- Ensure 2-Factor Authentication is enabled
- Verify SMTP settings for your provider

### Email "Not Configured" Warning
- Environment variables are not set
- Run `setup_email_config.ps1` before starting Flask
- Or set variables manually in the same PowerShell session

### WhatsApp Link Shows "Can't Download"
- If testing locally (127.0.0.1), recipient must be on same network
- For external sharing, deploy to public server

### PDF Not Found in WhatsApp
- Make sure PDF is generated first (click "Generate PDF")
- Check that uploads folder exists and has the file

---

## Security Best Practices

⚠️ **NEVER commit email passwords to Git!**

- Use environment variables (as configured above)
- Add `.env` files to `.gitignore`
- For production, use secure secret management
- Consider using services like SendGrid, Mailgun, or AWS SES for better deliverability

---

## Support

If you encounter issues:
1. Check the Flask console for error messages
2. Verify environment variables are set: `Get-ChildItem Env: | Where-Object { $_.Name -like '*SENDER*' }`
3. Test SMTP connection manually
