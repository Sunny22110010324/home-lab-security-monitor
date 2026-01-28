#!/usr/bin/env python3
"""
Check Project Structure
"""

import os
import sqlite3

print("📁 PROJECT STRUCTURE CHECK")
print("=" * 50)

# List of essential files
essential_files = [
    ('run_monitor.py', 'Main monitoring engine'),
    ('check_db_simple.py', 'Database verification tool'),
    ('quick_check.py', 'Quick database check'),
    ('requirements.txt', 'Python dependencies'),
    ('security_monitor.db', 'SQLite database'),
    ('src/dashboard.py', 'Flask dashboard server'),
    ('templates/dashboard.html', 'Dashboard HTML template'),
    ('venv/', 'Virtual environment'),
    ('README.md', 'Project documentation')
]

all_good = True

# Check each file
for filename, description in essential_files:
    if os.path.exists(filename):
        print(f'✅ {filename:25} {description}')
    else:
        print(f'❌ {filename:25} {description} - MISSING!')
        all_good = False

print()

# Show database stats
print("📊 YOUR PROJECT STATISTICS:")
try:
    conn = sqlite3.connect('security_monitor.db')
    cursor = conn.cursor()
    
    # Count system metrics
    cursor.execute('SELECT COUNT(*) FROM system_metrics')
    metrics_count = cursor.fetchone()[0]
    
    # Count security alerts
    cursor.execute('SELECT COUNT(*) FROM security_alerts')
    alerts_count = cursor.fetchone()[0]
    
    # Get latest disk reading
    cursor.execute('SELECT disk_percent FROM system_metrics ORDER BY timestamp DESC LIMIT 1')
    disk_percent = cursor.fetchone()[0]
    
    conn.close()
    
    print(f'  • System metrics collected: {metrics_count} records')
    print(f'  • Security alerts generated: {alerts_count} alerts')
    
    # Disk status warning
    if disk_percent > 95:
        print(f'  • Disk status: {disk_percent:.1f}% ⚠️ CRITICAL ISSUE DETECTED!')
    elif disk_percent > 90:
        print(f'  • Disk status: {disk_percent:.1f}% ⚠️ High usage')
    else:
        print(f'  • Disk status: {disk_percent:.1f}% ✅ Normal')
        
except sqlite3.Error as e:
    print(f'  • Database error: {e}')

print()
print("=" * 50)

if all_good:
    print("🎉 PROJECT COMPLETE & READY!")
    print("✅ All files present")
    print("✅ Database working")
    print("✅ Ready for GitHub and resume!")
else:
    print("⚠️  PROJECT INCOMPLETE")
    print("Some essential files are missing")
    print("Check the list above and create missing files")

print("=" * 50)