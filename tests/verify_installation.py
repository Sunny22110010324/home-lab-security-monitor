#!/usr/bin/env python3
"""
Verify installation and basic functionality
"""

import sys
import os
import sqlite3
from pathlib import Path

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("  ✅ Python version OK")
        return True
    else:
        print("  ❌ Python 3.8 or higher required")
        return False

def check_dependencies():
    """Check required packages"""
    print("\n🔍 Checking dependencies...")
    
    dependencies = [
        ('psutil', 'psutil'),
        ('flask', 'flask'),
        ('sqlite3', 'sqlite3')  # Built-in
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} not installed")
            all_ok = False
    
    return all_ok

def check_database():
    """Check database setup"""
    print("\n🔍 Checking database...")
    
    db_path = 'security_monitor.db'
    
    if not os.path.exists(db_path):
        print(f"  ⚠️  Database not found: {db_path}")
        print("  Run: python src/database/init_db.py")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['system_metrics', 'security_alerts']
        for table in required_tables:
            if table in tables:
                print(f"  ✅ Table exists: {table}")
            else:
                print(f"  ❌ Table missing: {table}")
                return False
        
        # Check sample data
        cursor.execute("SELECT COUNT(*) FROM system_metrics")
        metrics_count = cursor.fetchone()[0]
        print(f"  📊 Metrics records: {metrics_count}")
        
        cursor.execute("SELECT COUNT(*) FROM security_alerts")
        alerts_count = cursor.fetchone()[0]
        print(f"  🚨 Alert records: {alerts_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False

def check_project_structure():
    """Check project files and directories"""
    print("\n🔍 Checking project structure...")
    
    required_dirs = [
        'src',
        'src/database',
        'src/config',
        'templates',
        'static/css',
        'static/js',
        'tests',
        'logs'
    ]
    
    required_files = [
        'run_monitor.py',
        'requirements.txt',
        'src/monitor.py',
        'src/dashboard.py',
        'src/database/schema.sql',
        'templates/dashboard.html'
    ]
    
    all_ok = True
    
    for directory in required_dirs:
        if os.path.exists(directory) and os.path.isdir(directory):
            print(f"  ✅ Directory: {directory}/")
        else:
            print(f"  ❌ Missing directory: {directory}/")
            all_ok = False
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ File: {file}")
        else:
            print(f"  ❌ Missing file: {file}")
            all_ok = False
    
    return all_ok

def main():
    """Main verification function"""
    print("=" * 60)
    print("HOME LAB SECURITY MONITOR - INSTALLATION VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Database", check_database)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{check_name}")
        print("-" * 40)
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:30} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All checks passed! System is ready to run.")
        print("\nNext steps:")
        print("1. Start monitor: python run_monitor.py start")
        print("2. Start dashboard: python run_monitor.py dashboard")
        print("3. Open browser: http://localhost:5000")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)