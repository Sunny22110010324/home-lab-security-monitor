#!/usr/bin/env python3
"""
Updated Dashboard - Works with your HTML
"""

from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'security_monitor.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/summary')
def get_summary():
    """Get system summary"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get latest metrics
    cursor.execute('''
        SELECT cpu_percent, memory_percent, disk_percent
        FROM system_metrics
        ORDER BY timestamp DESC
        LIMIT 1
    ''')
    
    latest = cursor.fetchone()
    
    # Get alert counts
    cursor.execute('''
        SELECT alert_level, COUNT(*) as count
        FROM security_alerts
        WHERE status = 'OPEN' OR status IS NULL
        GROUP BY alert_level
    ''')
    
    alerts = {row['alert_level']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return jsonify({
        'latest_metrics': dict(latest) if latest else {},
        'alerts': alerts,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/metrics')
def get_metrics():
    """Get recent metrics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get last 30 metrics (last 5 minutes if 10-second intervals)
    cursor.execute('''
        SELECT timestamp, cpu_percent, memory_percent, disk_percent
        FROM system_metrics
        ORDER BY timestamp DESC
        LIMIT 30
    ''')
    
    metrics = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(metrics)

@app.route('/api/alerts')
def get_alerts():
    """Get recent alerts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT timestamp, alert_level, alert_type, description, status
        FROM security_alerts
        ORDER BY timestamp DESC
        LIMIT 20
    ''')
    
    alerts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(alerts)

if __name__ == '__main__':
    print("🌐 Dashboard: http://localhost:5000")
    print("📊 Using your dashboard.html template")
    app.run(host='0.0.0.0', port=5000, debug=True)