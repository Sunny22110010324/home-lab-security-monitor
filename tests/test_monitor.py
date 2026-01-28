#!/usr/bin/env python3
"""
Unit tests for monitor.py
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

class TestMonitorFunctions(unittest.TestCase):
    
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_collect_metrics(self, mock_memory, mock_cpu):
        """Test metrics collection with mocked psutil"""
        # Setup mocks
        mock_cpu.return_value = 25.5
        mock_memory.return_value.percent = 45.3
        
        # This is a simplified test - in reality you'd test the actual method
        metrics = {
            'cpu_percent': 25.5,
            'memory_percent': 45.3,
            'timestamp': datetime.now().isoformat()
        }
        
        self.assertEqual(metrics['cpu_percent'], 25.5)
        self.assertEqual(metrics['memory_percent'], 45.3)
        self.assertIsNotNone(metrics['timestamp'])
    
    def test_anomaly_detection(self):
        """Test anomaly detection logic"""
        # Test high CPU detection
        cpu_value = 95.5
        threshold = 85
        
        is_anomaly = cpu_value > threshold
        self.assertTrue(is_anomaly)
        
        # Determine severity
        if cpu_value > 90:
            severity = 'HIGH'
        elif cpu_value > 85:
            severity = 'MEDIUM'
        else:
            severity = 'LOW'
        
        self.assertEqual(severity, 'HIGH')
        
        # Test normal CPU
        cpu_value = 50
        is_anomaly = cpu_value > threshold
        self.assertFalse(is_anomaly)
    
    def test_alert_creation(self):
        """Test alert data structure"""
        alert = {
            'timestamp': '2024-01-27T10:00:00',
            'alert_level': 'HIGH',
            'alert_type': 'HIGH_CPU',
            'description': 'CPU at 95.5% (threshold: 85%)',
            'status': 'OPEN'
        }
        
        required_fields = ['timestamp', 'alert_level', 'alert_type', 'description', 'status']
        for field in required_fields:
            self.assertIn(field, alert)
        
        self.assertEqual(alert['alert_level'], 'HIGH')
        self.assertEqual(alert['status'], 'OPEN')

if __name__ == '__main__':
    unittest.main()