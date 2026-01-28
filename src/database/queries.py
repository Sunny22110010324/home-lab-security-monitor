#!/usr/bin/env python3
"""
Common database queries
"""

import sqlite3
from datetime import datetime, timedelta

def get_recent_metrics(hours=24, limit=100):
    """Get recent metrics"""
    conn = sqlite3.connect('security_monitor.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    
    cursor.execute('''
        SELECT * FROM system_metrics
        WHERE timestamp > ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (cutoff, limit))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results

def get_open_alerts():
    """Get all open alerts"""
    conn = sqlite3.connect('security_monitor.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM security_alerts
        WHERE status = 'OPEN'
        ORDER BY timestamp DESC
    ''')
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return results

def get_metrics_summary(hours=24):
    """Get metrics summary"""
    conn = sqlite3.connect('security_monitor.db')
    cursor = conn.cursor()
    
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    
    cursor.execute('''
        SELECT 
            AVG(cpu_percent) as avg_cpu,
            MAX(cpu_percent) as max_cpu,
            AVG(memory_percent) as avg_memory,
            MAX(memory_percent) as max_memory,
            COUNT(*) as count
        FROM system_metrics
        WHERE timestamp > ?
    ''', (cutoff,))
    
    result = cursor.fetchone()
    conn.close()
    
    return {
        'avg_cpu': result[0],
        'max_cpu': result[1],
        'avg_memory': result[2],
        'max_memory': result[3],
        'sample_count': result[4]
    }