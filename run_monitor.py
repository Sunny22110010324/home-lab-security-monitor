#!/usr/bin/env python3
"""
Home Lab Security Monitor - Main Runner
"""

import time
import sqlite3
import psutil
import os
from datetime import datetime

def setup_database():
    print("Setting up database...")
    conn = sqlite3.connect('security_monitor.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            hostname TEXT,
            cpu_percent REAL,
            memory_percent REAL,
            disk_percent REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            alert_level TEXT,
            alert_type TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database ready")

def collect_metrics():
    return {
        'timestamp': datetime.now().isoformat(),
        'hostname': os.environ.get('COMPUTERNAME', 'unknown'),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('C:\\').percent,
    }

def main():
    print("=" * 50)
    print("Home Lab Security Monitor")
    print("=" * 50)
    
    setup_database()
    print("\n🚀 Starting monitoring...\nPress Ctrl+C to stop\n")
    
    try:
        cycle = 0
        while True:
            cycle += 1
            print(f"📊 Cycle {cycle} - {datetime.now().strftime('%H:%M:%S')}")
            
            metrics = collect_metrics()
            print(f"  CPU: {metrics['cpu_percent']:.1f}%")
            print(f"  Memory: {metrics['memory_percent']:.1f}%")
            print(f"  Disk: {metrics['disk_percent']:.1f}%")
            
            conn = sqlite3.connect('security_monitor.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO system_metrics (timestamp, hostname, cpu_percent, memory_percent, disk_percent)
                VALUES (?, ?, ?, ?, ?)
            ''', (metrics['timestamp'], metrics['hostname'], metrics['cpu_percent'], 
                  metrics['memory_percent'], metrics['disk_percent']))
            
            if metrics['memory_percent'] > 85:
                cursor.execute('''
                    INSERT INTO security_alerts (timestamp, alert_level, alert_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (datetime.now().isoformat(), 'HIGH', 'HIGH_MEMORY', 
                      f"Memory: {metrics['memory_percent']:.1f}%"))
                print(f"  🚨 HIGH Memory Alert: {metrics['memory_percent']:.1f}%")
            
            if metrics['disk_percent'] > 90:
                cursor.execute('''
                    INSERT INTO security_alerts (timestamp, alert_level, alert_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (datetime.now().isoformat(), 'CRITICAL', 'HIGH_DISK', 
                      f"Disk: {metrics['disk_percent']:.1f}%"))
                print(f"  🚨 CRITICAL Disk Alert: {metrics['disk_percent']:.1f}%")
            
            conn.commit()
            conn.close()
            
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")

if __name__ == '__main__':
    main()