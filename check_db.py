#!/usr/bin/env python3
"""
Check Database - Simple Version
"""

import sqlite3
from datetime import datetime

print("=" * 60)
print("HOME LAB MONITOR - DATABASE CHECK")
print("=" * 60)

try:
    conn = sqlite3.connect('security_monitor.db')
    cursor = conn.cursor()
    
    # Show tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("\n📋 TABLES IN DATABASE:")
    for table in tables:
        print(f"  • {table[0]}")
    
    # System Metrics
    cursor.execute("SELECT COUNT(*) FROM system_metrics")
    metrics_count = cursor.fetchone()[0]
    print(f"\n📊 SYSTEM METRICS: {metrics_count} records")
    
    if metrics_count > 0:
        cursor.execute('''
            SELECT timestamp, cpu_percent, memory_percent, disk_percent 
            FROM system_metrics 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        print("\n  LATEST 5 RECORDS:")
        for row in cursor.fetchall():
            time_str = datetime.fromisoformat(row[0]).strftime('%H:%M:%S')
            print(f"    {time_str} | CPU: {row[1]:5.1f}% | Memory: {row[2]:5.1f}% | Disk: {row[3]:5.1f}%")
        
        # Statistics
        cursor.execute('''
            SELECT 
                AVG(cpu_percent), MIN(cpu_percent), MAX(cpu_percent),
                AVG(memory_percent), MIN(memory_percent), MAX(memory_percent),
                AVG(disk_percent), MIN(disk_percent), MAX(disk_percent)
            FROM system_metrics
        ''')
        stats = cursor.fetchone()
        print("\n  📈 STATISTICS:")
        print(f"    CPU:    Avg={stats[0]:5.1f}%  Min={stats[1]:5.1f}%  Max={stats[2]:5.1f}%")
        print(f"    Memory: Avg={stats[3]:5.1f}%  Min={stats[4]:5.1f}%  Max={stats[5]:5.1f}%")
        print(f"    Disk:   Avg={stats[6]:5.1f}%  Min={stats[7]:5.1f}%  Max={stats[8]:5.1f}% ⚠️")
    
    # Security Alerts
    cursor.execute("SELECT COUNT(*) FROM security_alerts")
    alerts_count = cursor.fetchone()[0]
    print(f"\n🚨 SECURITY ALERTS: {alerts_count} alerts")
    
    if alerts_count > 0:
        cursor.execute('''
            SELECT timestamp, alert_level, alert_type, description 
            FROM security_alerts 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        print("\n  RECENT ALERTS:")
        for alert in cursor.fetchall():
            time_str = datetime.fromisoformat(alert[0]).strftime('%H:%M')
            level = alert[1]
            color = {
                'CRITICAL': '\033[91m',  # Red
                'HIGH': '\033[93m',      # Yellow
                'MEDIUM': '\033[92m',    # Green
                'LOW': '\033[94m'        # Blue
            }.get(level, '\033[0m')
            reset = '\033[0m'
            print(f"    {time_str} | {color}[{level:8}]{reset} | {alert[2]:15} | {alert[3]}")
        
        # Alert summary
        cursor.execute('''
            SELECT alert_level, COUNT(*) 
            FROM security_alerts 
            GROUP BY alert_level 
            ORDER BY 
                CASE alert_level
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'LOW' THEN 4
                END
        ''')
        print("\n  📊 ALERT SUMMARY:")
        for level, count in cursor.fetchall():
            print(f"    {level:10}: {count:3} alerts")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE CHECK COMPLETE")
    print("=" * 60)
    
except sqlite3.OperationalError as e:
    print(f"\n❌ ERROR: {e}")
    print("\n💡 TIP: Run 'python run_monitor.py' first to create database")

except Exception as e:
    print(f"\n❌ UNEXPECTED ERROR: {e}")