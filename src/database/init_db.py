#!/usr/bin/env python3
"""
Database initialization
"""

import sqlite3
import os

def init_database():
    """Initialize the database"""
    db_path = 'security_monitor.db'
    
    # Remove old database if exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️  Removed old database")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('src/database/schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)
    
    # Insert sample data
    from datetime import datetime
    sample_time = datetime.now().isoformat()
    
    # Sample metrics
    cursor.execute('''
        INSERT INTO system_metrics 
        (timestamp, cpu_percent, memory_percent, disk_percent)
        VALUES (?, ?, ?, ?)
    ''', (sample_time, 25.5, 45.3, 67.8))
    
    # Sample alerts
    cursor.execute('''
        INSERT INTO security_alerts 
        (timestamp, alert_level, alert_type, description, status)
        VALUES 
        (?, 'LOW', 'SYSTEM_START', 'Monitoring system initialized', 'RESOLVED'),
        (?, 'MEDIUM', 'TEST_ALERT', 'This is a test alert', 'OPEN')
    ''', (sample_time, sample_time))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized at {db_path}")
    print("📊 Created tables: system_metrics, security_alerts, network_connections")
    print("📝 Inserted sample data")

if __name__ == '__main__':
    init_database()