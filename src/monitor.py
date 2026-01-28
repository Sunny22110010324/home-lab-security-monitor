#!/usr/bin/env python3
"""
Simplified Home Lab Monitor - Fixed Database Issues
"""

import time
from datetime import datetime
import sqlite3
import psutil
import socket
import platform

class HomeLabMonitor:
    def __init__(self, config_path='src/config/settings.yaml'):
        self.db_path = 'security_monitor.db'
        self.ensure_database()
        
    def ensure_database(self):
        """Make sure database and tables exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if tables exist, create if not
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                hostname TEXT,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL,
                network_sent_mb REAL,
                network_recv_mb REAL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                alert_level TEXT,
                alert_type TEXT,
                description TEXT,
                status TEXT DEFAULT 'OPEN'
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database tables verified")
    
    def get_db_connection(self):
        """Get fresh database connection"""
        return sqlite3.connect(self.db_path)
    
    def collect_metrics(self):
        """Collect system metrics"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'hostname': socket.gethostname(),
                'os': platform.system(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
            }
            
            # Try to get network stats (might fail on some systems)
            try:
                net_io = psutil.net_io_counters()
                metrics['network_sent_mb'] = net_io.bytes_sent / (1024**2)
                metrics['network_recv_mb'] = net_io.bytes_recv / (1024**2)
            except:
                metrics['network_sent_mb'] = 0
                metrics['network_recv_mb'] = 0
            
            return metrics
            
        except Exception as e:
            print(f"❌ Error collecting metrics: {e}")
            # Return minimal metrics
            return {
                'timestamp': datetime.now().isoformat(),
                'hostname': 'unknown',
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_percent': 0,
                'network_sent_mb': 0,
                'network_recv_mb': 0
            }
    
    def check_anomalies(self, metrics):
        """Check for security anomalies"""
        anomalies = []
        
        # Check CPU threshold
        if metrics['cpu_percent'] > 85:
            anomalies.append({
                'type': 'HIGH_CPU',
                'severity': 'HIGH' if metrics['cpu_percent'] > 90 else 'MEDIUM',
                'value': metrics['cpu_percent'],
                'threshold': 85
            })
        
        # Check memory threshold (your memory is at 89.2%!)
        if metrics['memory_percent'] > 85:
            anomalies.append({
                'type': 'HIGH_MEMORY',
                'severity': 'HIGH' if metrics['memory_percent'] > 90 else 'MEDIUM',
                'value': metrics['memory_percent'],
                'threshold': 85
            })
        
        # Check disk threshold (your disk is at 99.6%!)
        if metrics['disk_percent'] > 90:
            anomalies.append({
                'type': 'HIGH_DISK',
                'severity': 'CRITICAL' if metrics['disk_percent'] > 95 else 'HIGH',
                'value': metrics['disk_percent'],
                'threshold': 90
            })
        
        return anomalies
    
    def store_metrics(self, metrics):
        """Store metrics in database"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO system_metrics 
            (timestamp, hostname, cpu_percent, memory_percent, disk_percent,
             network_sent_mb, network_recv_mb)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics['timestamp'],
            metrics['hostname'],
            metrics['cpu_percent'],
            metrics['memory_percent'],
            metrics['disk_percent'],
            metrics.get('network_sent_mb', 0),
            metrics.get('network_recv_mb', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def create_alert(self, anomaly):
        """Create security alert"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO security_alerts 
            (timestamp, alert_level, alert_type, description, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            anomaly['severity'],
            anomaly['type'],
            f"{anomaly['type']}: {anomaly['value']:.1f}% (threshold: {anomaly['threshold']}%)",
            'OPEN'
        ))
        
        conn.commit()
        conn.close()
        print(f"🚨 Alert: {anomaly['type']} - {anomaly['severity']}")
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Monitoring cycle...")
        
        # Collect metrics
        metrics = self.collect_metrics()
        print(f"📊 CPU: {metrics['cpu_percent']:.1f}%, "
              f"Memory: {metrics['memory_percent']:.1f}%, "
              f"Disk: {metrics['disk_percent']:.1f}%")
        
        # Store metrics
        self.store_metrics(metrics)
        
        # Check for anomalies
        anomalies = self.check_anomalies(metrics)
        
        # Create alerts for anomalies
        for anomaly in anomalies:
            self.create_alert(anomaly)
        
        return {'metrics': metrics, 'anomalies': anomalies}
    
    def run_continuous(self, interval=30):
        """Run monitoring continuously with shorter interval for testing"""
        print("🚀 Starting Home Lab Monitor...")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.run_monitoring_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n🛑 Stopping monitor...")
        except Exception as e:
            print(f"\n❌ Error: {e}")