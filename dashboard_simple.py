#!/usr/bin/env python3
"""
Simple Dashboard - Put this in main folder
"""

from flask import Flask, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Home Lab Dashboard</title>
        <style>
            body { font-family: Arial; background: #0f172a; color: white; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .card { background: #1e293b; padding: 20px; margin: 10px 0; border-radius: 10px; }
            .stat { font-size: 24px; font-weight: bold; }
            .critical { color: #ff0000; }
            .warning { color: #ff9900; }
            .ok { color: #00cc00; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔒 Home Lab Security Monitor</h1>
            
            <div class="card">
                <h2>📊 System Status</h2>
                <div id="status">Loading...</div>
            </div>
            
            <div class="card">
                <h2>🚨 Recent Alerts</h2>
                <div id="alerts">Loading...</div>
            </div>
            
            <div class="card">
                <h2>📈 Database Info</h2>
                <div id="database">Loading...</div>
            </div>
        </div>
        
        <script>
            async function loadData() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    
                    // Update system status
                    document.getElementById('status').innerHTML = `
                        <div>CPU: <span class="stat ${getStatusClass(data.cpu, 85, 95)}">${data.cpu.toFixed(1)}%</span></div>
                        <div>Memory: <span class="stat ${getStatusClass(data.memory, 85, 95)}">${data.memory.toFixed(1)}%</span></div>
                        <div>Disk: <span class="stat critical">${data.disk.toFixed(1)}% ⚠️ CRITICAL</span></div>
                        <div>Last Update: ${new Date(data.timestamp).toLocaleTimeString()}</div>
                    `;
                    
                    // Update alerts
                    let alertsHtml = '';
                    if (data.alerts.length === 0) {
                        alertsHtml = '<div>✅ No recent alerts</div>';
                    } else {
                        data.alerts.forEach(alert => {
                            alertsHtml += `
                                <div style="margin: 10px 0; padding: 10px; background: #2d3748; border-radius: 5px;">
                                    <div><strong>${alert.alert_type}</strong> - <span class="${alert.alert_level.toLowerCase()}">${alert.alert_level}</span></div>
                                    <div>${alert.description}</div>
                                    <div style="font-size: 12px; color: #94a3b8;">${new Date(alert.timestamp).toLocaleString()}</div>
                                </div>
                            `;
                        });
                    }
                    document.getElementById('alerts').innerHTML = alertsHtml;
                    
                    // Update database info
                    document.getElementById('database').innerHTML = `
                        <div>📊 Total Metrics: ${data.metrics_count}</div>
                        <div>🚨 Total Alerts: ${data.alerts_count}</div>
                        <div>⏰ First Record: ${data.first_record ? new Date(data.first_record).toLocaleDateString() : 'N/A'}</div>
                        <div>🕐 Last Record: ${data.last_record ? new Date(data.last_record).toLocaleDateString() : 'N/A'}</div>
                    `;
                    
                } catch (error) {
                    console.error('Error loading data:', error);
                    document.getElementById('status').innerHTML = 'Error loading data';
                }
            }
            
            function getStatusClass(value, warning, critical) {
                if (value > critical) return 'critical';
                if (value > warning) return 'warning';
                return 'ok';
            }
            
            // Load data immediately
            loadData();
            
            // Refresh every 5 seconds
            setInterval(loadData, 5000);
        </script>
    </body>
    </html>
    '''

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('security_monitor.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/status')
def get_status():
    """Get system status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest metrics
    cursor.execute('''
        SELECT timestamp, cpu_percent, memory_percent, disk_percent
        FROM system_metrics
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    latest = cursor.fetchone()
    
    # Get recent alerts
    cursor.execute('''
        SELECT timestamp, alert_level, alert_type, description
        FROM security_alerts
        ORDER BY timestamp DESC
        LIMIT 10
    ''')
    alerts = [dict(row) for row in cursor.fetchall()]
    
    # Get database stats
    cursor.execute('SELECT COUNT(*) FROM system_metrics')
    metrics_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM security_alerts')
    alerts_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(timestamp) FROM system_metrics')
    first_record = cursor.fetchone()[0]
    
    cursor.execute('SELECT MAX(timestamp) FROM system_metrics')
    last_record = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'cpu': latest['cpu_percent'] if latest else 0,
        'memory': latest['memory_percent'] if latest else 0,
        'disk': latest['disk_percent'] if latest else 0,
        'timestamp': latest['timestamp'] if latest else datetime.now().isoformat(),
        'alerts': alerts,
        'metrics_count': metrics_count,
        'alerts_count': alerts_count,
        'first_record': first_record,
        'last_record': last_record
    })

if __name__ == '__main__':
    print("🌐 Simple Dashboard: http://localhost:5001")
    print("📊 Monitoring your system with 100% disk usage!")
    app.run(host='0.0.0.0', port=5001, debug=True)