import re
from database import execute_query

def scan_for_ips():
    """
    Pulls all server logs and uses Regex to identify and categorize IP addresses.
    Returns a list of suspicious external IP addresses found.
    """
    print("\n--- 🔍 REGEX SCAN 1: ANALYZING NETWORK TRAFFIC ---")
    logs = execute_query("SELECT timestamp, ip_address, username, action FROM server_logs")
    
    # REGEX PATTERN FOR AN IPv4 ADDRESS:
    # \b     = Word boundary (ensures we don't grab digits inside longer words)
    # \d{1,3} = A digit (0-9) repeated between 1 and 3 times
    # \.     = A literal dot (we must escape it with '\' because a bare '.' means ANY character in regex!)
    ip_pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    
    suspicious_ips = set() # We use a Python Set to automatically avoid duplicate IPs
    
    for log in logs:
        timestamp, ip, user, action = log
        
        # re.search scans the string and returns a Match object if the pattern is found
        match = re.search(ip_pattern, ip)
        if match:
            # .group() extracts the actual matched string from the Match object
            found_ip = match.group()
            
            # Corporate internal networks usually start with '192.168.' or '10.0.'
            # Anything else penetrating our server is an external intruder!
            if found_ip.startswith("192.168.") or found_ip.startswith("10.0."):
                print(f"  🟢 [INTERNAL] {timestamp} | IP: {found_ip:<15} | User: {user}")
            else:
                print(f"  🚨 [EXTERNAL ANOMALY] {timestamp} | IP: {found_ip:<15} | User: {user} | Action: {action}")
                suspicious_ips.add(found_ip)
                
    return list(suspicious_ips)

def scan_for_exfiltrated_files():
    """
    Uses Regex to search log actions for hidden file downloads (.zip, .pdf, .sql, etc.).
    """
    print("\n--- 🔍 REGEX SCAN 2: HUNTING EXFILTRATED FILES ---")
    logs = execute_query("SELECT timestamp, username, action FROM server_logs")
    
    # REGEX PATTERN FOR FILE NAMES:
    # \w+       = One or more "word characters" (letters, numbers, or underscores for the filename)
    # \.        = A literal dot separating the name from the extension
    # (?:zip|pdf|sql|tar|csv) = A non-capturing group matching any of these specific extensions
    file_pattern = r"\b\w+\.(?:zip|pdf|sql|tar|csv)\b"
    
    for log in logs:
        timestamp, user, action = log
        
        # re.findall returns a clean Python list of EVERY matching string found in the text
        found_files = re.findall(file_pattern, action, re.IGNORECASE)
        
        if found_files:
            for file_name in found_files:
                print(f"  📦 FILE DETECTED: {file_name:<25} | Downloaded by: {user} at {timestamp}")

def scan_employee_emails():
    """
    Scans the staff table using Regex to verify email formatting and domain security.
    """
    print("\n--- 🔍 REGEX SCAN 3: VERIFYING STAFF EMAIL FORMATS ---")
    employees = execute_query("SELECT full_name, email FROM employees")
    
    # STANDARD EMAIL REGEX PATTERN: [username]@[domain].[extension]
    # ^ and $ force the regex to match the entire string from beginning to end
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    
    for name, email in employees:
        if re.match(email_pattern, email):
            print(f"  ✅ Valid corporate format: {name:<15} -> {email}")
        else:
            print(f"  ❌ INVALID OR CORROPT EMAIL: {name:<15} -> {email}")

# --- TESTING OUR FORENSIC SCANNER ---
if __name__ == "__main__":
    print("🕵️‍♂️ BOOTING UP FORENSIC REGEX SCANNER...")
    
    # Run the network scan and save suspicious IPs
    intruder_ips = scan_for_ips()
    print(f"\n💡 SUMMARY: Found {len(intruder_ips)} unauthorized external IP address(es): {intruder_ips}")
    
    # Run the file exfiltration and email scans
    scan_for_exfiltrated_files()
    scan_employee_emails()