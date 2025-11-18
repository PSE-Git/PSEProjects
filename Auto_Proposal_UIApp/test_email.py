import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "precisesmart.enterprises@gmail.com"
sender_password = "ozqwcpfyfjgipphy"  # App password without spaces
recipient_email = "praneshkrishnan.b@gmail.com"

# PDF file
pdf_filename = "Body_Fit_Gym_6.pdf"
pdf_path = os.path.join("uploads", pdf_filename)

print(f"Checking if PDF exists: {pdf_path}")
if not os.path.exists(pdf_path):
    print(f"ERROR: PDF file not found at {pdf_path}")
    exit(1)

print(f"✓ PDF found: {pdf_path}")

# Create message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = "Proposal: Body Fit Gym"

# Email body
body = """
Dear Client,

Please find attached the proposal for your project: Body Fit Gym

Project Details:
- Project Type: Gym Interior Design
- Professional proposal with detailed BOQ

If you have any questions, please feel free to contact us.

Best regards,
Precise Smart Enterprises
"""

msg.attach(MIMEText(body, 'plain'))

# Attach PDF
print(f"Attaching PDF: {pdf_filename}")
with open(pdf_path, 'rb') as f:
    pdf_data = f.read()
    pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
    msg.attach(pdf_attachment)

print(f"PDF attached ({len(pdf_data)} bytes)")

# Send email
try:
    print(f"\nConnecting to {smtp_server}:{smtp_port}...")
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)  # Show detailed debug output
    
    print("Starting TLS...")
    server.starttls()
    
    print(f"Logging in as {sender_email}...")
    server.login(sender_email, sender_password)
    
    print(f"Sending email to {recipient_email}...")
    server.send_message(msg)
    
    print("Closing connection...")
    server.quit()
    
    print("\n" + "="*50)
    print("✓ EMAIL SENT SUCCESSFULLY!")
    print("="*50)
    print(f"To: {recipient_email}")
    print(f"Subject: Proposal: Body Fit Gym")
    print(f"Attachment: {pdf_filename}")
    print("\nPlease check your inbox (and spam folder).")
    
except smtplib.SMTPAuthenticationError as e:
    print("\n" + "="*50)
    print("✗ AUTHENTICATION FAILED")
    print("="*50)
    print(f"Error: {e}")
    print("\nPlease check:")
    print("1. Email address is correct")
    print("2. App password is correct (no spaces)")
    print("3. 2-Factor Authentication is enabled on Gmail")
    print("4. App password was generated at: https://myaccount.google.com/apppasswords")
    
except Exception as e:
    print("\n" + "="*50)
    print("✗ ERROR SENDING EMAIL")
    print("="*50)
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
