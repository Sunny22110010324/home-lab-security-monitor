#!/usr/bin/env python3
"""
Alert management system
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

class AlertSystem:
    def __init__(self, config):
        self.config = config
        
    def send_email_alert(self, alert):
        """Send email alert"""
        if not self.config.get('email_enabled', False):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_from']
            msg['To'] = self.config['email_to']
            msg['Subject'] = f"Security Alert: {alert['alert_type']}"
            
            body = f"""
            Security Alert Detected
            
            Type: {alert['alert_type']}
            Severity: {alert['severity']}
            Time: {alert['timestamp']}
            Description: {alert['description']}
            
            Home Lab Security Monitor
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(
                self.config['email_server'],
                self.config['email_port']
            )
            server.starttls()
            server.login(
                self.config['email_username'],
                self.config['email_password']
            )
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"❌ Email alert failed: {e}")
            return False
    
    def send_slack_alert(self, alert):
        """Send Slack alert"""
        # This would be implemented with Slack webhooks
        # For now, just print
        print(f"📢 Slack Alert: {alert['alert_type']} - {alert['severity']}")
        return True