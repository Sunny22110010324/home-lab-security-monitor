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
<img src="https://raw.githubusercontent.com/Sunny22110010324/home-lab-security-monitor/main/screenshots/terminal1-monitor.png" width="400" height="300" alt="Monitor Terminal Output">

**Running the security monitor with real-time system metrics**
**Output Explanation:**
📊 Cycle X: Monitoring cycle number and timestamp

1. CPU: XX.X%: Current CPU usage percentage

2. Memory: XX.X%: Current memory usage percentage

3. Disk: XX.X%: Current disk usage percentage

4. 🚨 Alert: Generated when thresholds are exceeded (Memory >85%, Disk >90%)

5. Press Ctrl+C to stop monitoring

**Terminal 2: Start the Dashboard**
```bash
cd src
python dashboard.py
```
<img src="https://raw.githubusercontent.com/Sunny22110010324/home-lab-security-monitor/main/screenshots/terminal2-dashboard.png" width="400" height="300" alt="Monitor Terminal Output">

**Expected Output:**
```bash
🌐 Dashboard: http://localhost:5000
📊 Using your dashboard.html template
 * Serving Flask app 'dashboard'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Sunny22110010324/home-lab-security-monitor/main/screenshots/dashboard-web.png" width="400" alt="Dashboard Screenshot 1">
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Sunny22110010324/home-lab-security-monitor/main/screenshots/dashboard-web%201.png" width="400" alt="Dashboard Screenshot 2">
    </td>
  </tr>
</table>

**Terminal 3: Check Database**
```bash
# Method 1: Using check_db_simple.py
python check_db_simple.py

# Method 2: Quick check
python quick_check.py
```
<img src="https://raw.githubusercontent.com/Sunny22110010324/home-lab-security-monitor/main/screenshots/terminal3-database.png" width="400" height="300" alt="Database">

**Expected Output (quick_check.py):**

📊 Total metrics: 26
⏰ Latest: CPU=21.7%, Memory=85.3%, Disk=99.9%

✅ Database accessibleOutput Explanation:
1. Total metrics: Number of system measurements stored
2. Latest: Most recent CPU, Memory, Disk readings
3. Total alerts: Number of security alerts generated
4. Database accessible: Confirms database is working

