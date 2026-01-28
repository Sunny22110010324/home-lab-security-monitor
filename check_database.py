#!/usr/bin/env python3
"""
Check Database Contents
"""

import sqlite3
from datetime import datetime

def check_database():
    print("🔍 Checking Database Contents")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('security_monitor.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("\n📋 Tables in database:")
        for table in tables:
            print(f"  • {table[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM system_metrics")
        count = cursor.fetchone()[0]
        print(f"\n📊 System Metrics: {count} records")
        
        if count > 0:
            cursor.execute("SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM system_metrics ORDER BY timestamp DESC LIMIT 3")
            rows = cursor.fetchall()
            print("\n  Latest 3 records:")
            for row in rows:
                time_str = datetime.fromisoformat(row[0]).strftime('%H:%M:%S')
                print(f"    {time_str} - CPU: {row[1]:.1f}%, Memory: {row[2]:.1f}%, Disk: {row[3]:.1f}%")
        
        cursor.execute("SELECT COUNT(*) FROM security_alerts")
        alert_count = cursor.fetchone()[0]
        print(f"\n🚨 Security Alerts: {alert_count} alerts")
        
        if alert_count > 0:
            cursor.execute("SELECT timestamp, alert_level, alert_type, description FROM security_alerts ORDER BY timestamp DESC LIMIT 5")
            alerts = cursor.fetchall()
            print("\n  Latest alerts:")
            for alert in alerts:
                time_str = datetime.fromisoformat(alert[0]).strftime('%H:%M:%S')
                print(f"    {time_str} - [{alert[1]}] {alert[2]}: {alert[3]}")
        
        conn.close()
        print("\n✅ Database check complete")
        
    except sqlite3.OperationalError:
        print("❌ Database not found or empty")
        print("💡 Run 'python run_monitor.py' first to create database")

if __name__ == '__main__':
    check_database()