# 🔒 Home Lab Security Monitoring System

A comprehensive cybersecurity project that monitors system health, detects anomalies, and provides real-time security alerts with a professional web dashboard.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Security](https://img.shields.io/badge/Cybersecurity-Project-red)

## 📋 Features

- **Real-time Monitoring**: CPU, Memory, Disk usage with 10-second intervals
- **Security Alerts**: Automatic detection of critical system issues
- **Professional Dashboard**: Web interface with real-time charts and alerts
- **Database Storage**: SQLite database with historical metrics and alerts
- **Threshold-based Alerting**: Configurable thresholds for different severity levels

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/Mac OS

### Installation
```bash
# Clone or download the project
cd home-lab-security-monitor

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install psutil flask

📊 Running the System
Terminal 1: Start the Monitor
python run_monitor.py



  Output Explanation:

📊 Cycle X: Monitoring cycle number and timestamp

CPU: XX.X%: Current CPU usage percentage

Memory: XX.X%: Current memory usage percentage

Disk: XX.X%: Current disk usage percentage

🚨 Alert: Generated when thresholds are exceeded (Memory >85%, Disk >90%)

Press Ctrl+C to stop monitoring

Terminal 2: Start the Dashboard
cd src
python dashboard.py

Expected Output:

🌐 Dashboard: http://localhost:5000
📊 Using your dashboard.html template
 * Serving Flask app 'dashboard'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit

Terminal 3: Check Database
# Method 1: Using check_db_simple.py
python check_db_simple.py

# Method 2: Quick check
python quick_check.py

# Method 3: One-liner
python -c "import sqlite3; conn=sqlite3.connect('security_monitor.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM system_metrics'); print(f'📊 Records: {cur.fetchone()[0]}'); conn.close()"
Expected Output (check_db_simple.py):
🔍 Checking Database...
========================================
📊 Total metrics: 26
⏰ Latest:
   Time: 14:58:05
   CPU: 21.7%
   Memory: 85.3%
   Disk: 99.9%
🚨 Total alerts: 32
✅ Database accessible

Expected Output (quick_check.py):

📊 Total metrics: 26
⏰ Latest: CPU=21.7%, Memory=85.3%, Disk=99.9%
✅ Database accessibleOutput Explanation:

Total metrics: Number of system measurements stored

Latest: Most recent CPU, Memory, Disk readings

Total alerts: Number of security alerts generated

Database accessible: Confirms database is working

