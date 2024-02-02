import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import django
from django.core.management import execute_from_command_line
from datetime import datetime


django_project_path = os.path.dirname(os.path.abspath(__file__))

# Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sharma_Academy.settings')

# Configure the Django app
django.setup()

# Set the email configuration
email_config = {
    'sender_email': 'afsarbabu010124@gmail.com',
    'receiver_email': 'pranav.lohar@codiatic.com',
    'email_password': 'wlzs pway sorw hhuz',
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
}

# Backup and email function
def backup_and_email():
    # Create a backup of the SQLite database
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    backup_path = os.path.join(django_project_path, backup_filename)
    
    # Run Django management command to dumpdata
    # Change this line
    
    try:
        with open(backup_path, 'w') as backup_file:
            subprocess.run(
                ['python', 'manage.py', 'dumpdata', '--exclude', 'auth.permission', '--exclude', 'contenttypes', '--indent', '2'],
                stdout=backup_file,
                stderr=subprocess.PIPE,  # Capture any error messages
                text=True  # Specify text mode for stdout and stderr
            )
    except subprocess.CalledProcessError as e:
        print(f"Error while running dumpdata command: {e.stderr}")
    
    send_email(backup_filename, backup_path)
    print("backup taken and email sent successfully.")
    os.remove(backup_path)

# Email sending function
def send_email(attachment_filename, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = email_config['sender_email']
    msg['To'] = email_config['receiver_email']
    msg['Subject'] = 'Django SQLite Backup '+datetime.now().strftime('%Y%m%d%H%M%S')

    # Attach the backup file to the email
    with open(attachment_path, 'rb') as file:
        attach = MIMEApplication(file.read(),_subtype="json")
        attach.add_header('Content-Disposition','attachment',filename=str(attachment_filename))
        msg.attach(attach)

    # Establish a connection to the SMTP server and send the email
    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['sender_email'], email_config['email_password'])
        server.sendmail(email_config['sender_email'], email_config['receiver_email'], msg.as_string())

if __name__ == '__main__':
    backup_and_email()
