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
```
**📊 Running the System**
**Terminal 1: Start the Monitor**
```bash
python run_monitor.py
```
**Expected Output:**

**Terminal 2: Start the Dashboard**
```bash
cd src
python dashboard.py
```
**Terminal 3: Check Database**
```bash
# Method 1: Using check_db_simple.py
python check_db_simple.py

# Method 2: Quick check
python quick_check.py

# Method 3: One-liner
python -c \"import sqlite3; conn=sqlite3.connect('security_monitor.db'); cur=conn.cursor(); cur.execute('SELECT COUNT(*) FROM system_metrics'); print(f'📊 Records: {cur.fetchone()[0]}'); conn.close()\"
```
