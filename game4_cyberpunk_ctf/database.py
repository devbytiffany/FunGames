import sqlite3
import hashlib
import os

DB_FILE = "nexus_corp.db"

def get_hash(password):
    """Helper function to convert a plaintext password into a SHA-256 hash."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_db():
    """
    Creates the NexusCorp database tables and populates them with mock forensic data.
    If the database already exists, it removes it to start fresh.
    """
    # Remove existing database file if it exists so we can generate a clean state
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    print("🔌 Connecting to NexusCorp database server...")
    # 1. Open a connection to the SQLite file
    conn = sqlite3.connect(DB_FILE)
    # 2. Create a Cursor object to execute SQL commands
    cursor = conn.cursor()
    
    print("🧱 Building relational database tables...")
    
    # --- TABLE 1: EMPLOYEES ---
    cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL,
        department TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """)
    
    # --- TABLE 2: SERVER LOGS ---
    cursor.execute("""
    CREATE TABLE server_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        ip_address TEXT NOT NULL,
        username TEXT,
        action TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)
    
    # --- TABLE 3: CREDENTIALS ---
    cursor.execute("""
    CREATE TABLE credentials (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL,
        access_level INTEGER NOT NULL
    );
    """)
    
    print("💉 Injecting corporate staff records and hidden clues...")
    
    # Populate Employees (Notice our suspicious employee 'n_ryder')
    employees_data = [
        ("t_stark", "Tony Stark", "Engineering", "t.stark@nexuscorp.internal"),
        ("a_smasher", "Adam Smasher", "Security", "a.smasher@nexuscorp.internal"),
        ("n_ryder", "Nyx Ryder", "Network Ops", "n.ryder@nexuscorp.internal"), # THE MOLE!
        ("s_connor", "Sarah Connor", "Logistics", "s.connor@nexuscorp.internal"),
        ("e_alderson", "Elliot Alderson", "Cybersecurity", "e.alderson@nexuscorp.internal")
    ]
    # Use parameterized queries (?) to insert multiple rows cleanly
    cursor.executemany("INSERT INTO employees (username, full_name, department, email) VALUES (?, ?, ?, ?)", employees_data)
    
    # Populate Credentials with SHA-256 Hashes
    # In real systems, you NEVER save plaintext passwords! We store the hash.
    credentials_data = [
        ("t_stark", get_hash("ironman123"), 3),
        ("a_smasher", get_hash("destroyer"), 2),
        ("n_ryder", get_hash("shadowrun"), 1), # We will crack 'shadowrun' later!
        ("s_connor", get_hash("skynet2029"), 2),
        ("e_alderson", get_hash("mrrobot"), 4)
    ]
    cursor.executemany("INSERT INTO credentials (username, password_hash, access_level) VALUES (?, ?, ?)", credentials_data)
    
    # Populate Server Logs (Mixing normal noise with unauthorized access attempts)
    logs_data = [
        ("2026-07-05 08:14:22", "192.168.1.15", "t_stark", "LOGIN_SUCCESS", "OK"),
        ("2026-07-05 09:02:11", "10.0.0.42", "s_connor", "FILE_READ: shipment_manifest.pdf", "OK"),
        ("2026-07-05 11:45:00", "192.168.1.88", "a_smasher", "FIREWALL_CONFIG_UPDATE", "OK"),
        # SUSPICIOUS LOGS: Someone using an external/unusual IP at 3 AM trying to access Project Icarus!
        ("2026-07-06 03:12:05", "185.220.101.7", "unknown", "FAILED_LOGIN_ATTEMPT: admin", "FAIL"),
        ("2026-07-06 03:14:18", "185.220.101.7", "n_ryder", "LOGIN_SUCCESS", "OK"),
        ("2026-07-06 03:15:44", "185.220.101.7", "n_ryder", "UNAUTHORIZED_DOWNLOAD: project_icarus_core.zip", "FLAGGED"),
        ("2026-07-06 03:16:02", "185.220.101.7", "n_ryder", "LOG_CLEAR_ATTEMPT", "DENIED"),
        ("2026-07-06 08:30:10", "192.168.1.50", "e_alderson", "SYSTEM_DIAGNOSTIC_RUN", "OK")
    ]
    cursor.executemany("INSERT INTO server_logs (timestamp, ip_address, username, action, status) VALUES (?, ?, ?, ?, ?)", logs_data)
    
    # 3. Commit the transaction to save changes to the file
    conn.commit()
    # 4. Close the connection
    conn.close()
    
    print("✅ Database successfully initialized! File created: " + DB_FILE)

def execute_query(query, params=()):
    """
    Helper function to safely execute a SQL query and return all matching rows.
    We will use this in our game loop!
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# --- TESTING OUR ENGINE ---
if __name__ == "__main__":
    initialize_db()
    
    print("\n--- 🕵️‍♂️ FORENSIC TEST: QUERYING SUSPICIOUS LOGS ---")
    # Let's run a test SQL query to find all flagged actions
    test_query = "SELECT timestamp, ip_address, username, action FROM server_logs WHERE status = 'FLAGGED'"
    flagged_logs = execute_query(test_query)
    
    for log in flagged_logs:
        print(f"🚨 ALERT [{log[0]}] IP: {log[1]} | User: {log[2]} | Action: {log[3]}")