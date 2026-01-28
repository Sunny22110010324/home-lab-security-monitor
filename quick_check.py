# quick_check.py
import sqlite3
conn = sqlite3.connect('security_monitor.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM system_metrics')
count = cursor.fetchone()[0]
print(f'📊 Total metrics: {count}')
cursor.execute('SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM system_metrics ORDER BY timestamp DESC LIMIT 1')
latest = cursor.fetchone()
if latest:
    print(f'⏰ Latest: CPU={latest[1]}%, Memory={latest[2]}%, Disk={latest[3]}%')
conn.close()
print('✅ Database accessible')