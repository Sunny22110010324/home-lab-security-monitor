#!/usr/bin/env python3
"""
Slack notification integration
"""

import requests
import json

class SlackNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def send_alert(self, alert):
        """Send alert to Slack"""
        if not self.webhook_url:
            return False
        
        message = {
            "text": f"🚨 Security Alert: {alert['alert_type']}",
            "attachments": [{
                "color": self._get_color(alert['severity']),
                "fields": [
                    {"title": "Severity", "value": alert['severity'], "short": True},
                    {"title": "Time", "value": alert['timestamp'], "short": True},
                    {"title": "Description", "value": alert['description'], "short": False}
                ]
            }]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                data=json.dumps(message),
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Slack notification failed: {e}")
            return False
    
    def _get_color(self, severity):
        """Get color based on severity"""
        colors = {
            'CRITICAL': '#ff0000',
            'HIGH': '#ff3300',
            'MEDIUM': '#ff9900',
            'LOW': '#00cc00'
        }
        return colors.get(severity, '#cccccc')