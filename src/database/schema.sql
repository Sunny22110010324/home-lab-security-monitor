-- Home Lab Security Monitor Database Schema

-- System metrics table
CREATE TABLE IF NOT EXISTS system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    hostname TEXT,
    cpu_percent REAL,
    memory_percent REAL,
    disk_percent REAL,
    network_sent_mb REAL,
    network_recv_mb REAL
);

-- Security alerts table
CREATE TABLE IF NOT EXISTS security_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    alert_level TEXT,
    alert_type TEXT,
    description TEXT,
    details TEXT,
    status TEXT DEFAULT 'OPEN',
    assigned_to TEXT,
    resolved_at DATETIME
);

-- Network connections table
CREATE TABLE IF NOT EXISTS network_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    local_address TEXT,
    remote_address TEXT,
    local_port INTEGER,
    remote_port INTEGER,
    status TEXT,
    pid INTEGER,
    process_name TEXT
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON system_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON security_alerts(timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON security_alerts(status);