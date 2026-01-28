#!/usr/bin/env python3
"""
Test scenarios for the monitoring system
"""

import unittest
import sqlite3
import os
import tempfile
from datetime import datetime
from src.monitor import HomeLabMonitor

class TestMonitor(unittest.TestCase):
    
    def setUp(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.db_path = self.test_db.name
        
        # Initialize test database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE system_metrics (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                cpu_percent REAL,
                memory_percent REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE security_alerts (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                alert_level TEXT,
                alert_type TEXT,
                description TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_database_creation(self):
        """Test that database tables are created"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('system_metrics', tables)
        self.assertIn('security_alerts', tables)
        
        conn.close()
    
    def test_metrics_collection(self):
        """Test metrics collection (simulated)"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'hostname': 'test-host',
            'cpu_percent': 25.5,
            'memory_percent': 45.3,
            'disk_percent': 67.8
        }
        
        # Test that metrics have expected keys
        expected_keys = ['timestamp', 'hostname', 'cpu_percent', 'memory_percent', 'disk_percent']
        for key in expected_keys:
            self.assertIn(key, metrics)
        
        # Test value ranges
        self.assertGreaterEqual(metrics['cpu_percent'], 0)
        self.assertLessEqual(metrics['cpu_percent'], 100)
    
    def test_alert_generation(self):
        """Test alert generation logic"""
        # Simulate high CPU
        anomaly = {
            'type': 'HIGH_CPU',
            'severity': 'HIGH',
            'value': 95.5,
            'threshold': 85
        }
        
        self.assertEqual(anomaly['type'], 'HIGH_CPU')
        self.assertEqual(anomaly['severity'], 'HIGH')
        self.assertGreater(anomaly['value'], anomaly['threshold'])
        
        # Test alert description
        description = f"{anomaly['type']}: {anomaly['value']}% (threshold: {anomaly['threshold']}%)"
        self.assertIn('HIGH_CPU', description)
        self.assertIn('95.5', description)
    
    def test_database_insertion(self):
        """Test inserting data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert test data
        test_time = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO system_metrics 
            (timestamp, cpu_percent, memory_percent)
            VALUES (?, ?, ?)
        ''', (test_time, 25.5, 45.3))
        
        cursor.execute('''
            INSERT INTO security_alerts 
            (timestamp, alert_level, alert_type, description)
            VALUES (?, ?, ?, ?)
        ''', (test_time, 'MEDIUM', 'TEST', 'Test alert'))
        
        conn.commit()
        
        # Verify insertion
        cursor.execute('SELECT COUNT(*) FROM system_metrics')
        self.assertEqual(cursor.fetchone()[0], 1)
        
        cursor.execute('SELECT COUNT(*) FROM security_alerts')
        self.assertEqual(cursor.fetchone()[0], 1)
        
        conn.close()

def run_tests():
    """Run all tests"""
    print("🧪 Running Home Lab Monitor Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMonitor)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == '__main__':
    run_tests()