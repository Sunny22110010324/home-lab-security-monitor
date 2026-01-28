#!/usr/bin/env python3
"""
Simple Database Checker
"""

import sqlite3

print("🔍 Checking Database...")
print("=" * 40)

try:
    conn = sqlite3.connect('security_monitor.db')
    cursor = conn.cursor()
    
    # Count records
    cursor.execute('SELECT COUNT(*) FROM system_metrics')
    count = cursor.fetchone()[0]
    print(f'📊 Total metrics: {count}')
    
    # Get latest record
    cursor.execute('''
        SELECT timestamp, cpu_percent, memory_percent, disk_percent 
        FROM system_metrics 
        ORDER BY timestamp DESC 
        LIMIT 1
    ''')
    latest = cursor.fetchone()
    
    if latest:
        print(f'⏰ Latest:')
        print(f'   Time: {latest[0][11:19]}')
        print(f'   CPU: {latest[1]:.1f}%')
        print(f'   Memory: {latest[2]:.1f}%')
        print(f'   Disk: {latest[3]:.1f}%')
    
    # Get alert count
    cursor.execute('SELECT COUNT(*) FROM security_alerts')
    alerts = cursor.fetchone()[0]
    print(f'🚨 Total alerts: {alerts}')
    
    conn.close()
    print('✅ Database accessible')
    
except sqlite3.OperationalError as e:
    print(f'❌ Database error: {e}')
    print('💡 Run: python run_monitor.py first')