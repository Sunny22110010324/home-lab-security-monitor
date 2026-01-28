#!/usr/bin/env python3
"""
Email notification integration
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self, config):
        self.config = config
    
    def send_alert(self, alert):
        """Send email alert"""
        if not self.config.get('email_enabled', False):
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg['Subject'] = f"[{alert['severity']}] Security Alert: {alert['alert_type']}"
            
            # Create email body
            body = f"""
            ===============================
            SECURITY ALERT NOTIFICATION
            ===============================
            
            Alert Type: {alert['alert_type']}
            Severity: {alert['severity']}
            Time: {alert['timestamp']}
            
            Description:
            {alert['description']}
            
            Action Required:
            Please investigate this alert in the Home Lab Security Dashboard.
            
            -------------------------------
            Home Lab Security Monitor
            Automated Notification System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config['email_server'], self.config['email_port'])
            server.starttls()
            server.login(self.config['email_username'], self.config['email_password'])
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Email alert sent to {self.config['email_to']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email alert: {e}")
            return False