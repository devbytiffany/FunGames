import sys
import time

# Importing our custom cybersecurity modules
from database import initialize_db, execute_query
from scanner import scan_for_ips, scan_for_exfiltrated_files, scan_employee_emails
from cracker import crack_password, audit_all_passwords

def print_header():
    """Prints the cyberpunk OS terminal banner."""
    print("\n" + "="*60)
    print(" 🕹️  NEXUS-OS FORENSIC INVESTIGATION TERMINAL v2.0  🕹️ ")
    print("="*60)
    print(" STATUS: CRITICAL BREACH DETECTED IN CORPORATE DATABASE")
    print(" MISSION: Identify unauthorized IPs, locate stolen files,")
    print("          and crack the mole's SHA-256 encrypted password.")
    print("="*60)

def run_custom_sql_query():
    """Allows the detective to execute custom SQL queries against the database."""
    print("\n--- 💻 DIRECT SQL QUERY CONSOLE ---")
    print("Available tables: 'employees', 'server_logs', 'credentials'")
    print("Example: SELECT username, action FROM server_logs WHERE status = 'FLAGGED'")
    
    query = input("\nSQL> ").strip()
    if not query:
        print("❌ Empty query. Returning to menu.")
        return
        
    try:
        results = execute_query(query)
        if not results:
            print("💡 Query executed successfully. No matching rows returned.")
        else:
            print(f"\n✅ Returned {len(results)} row(s):")
            for row in results[:15]: # Limit display to 15 rows to prevent terminal flooding
                print("  ->", row)
    except Exception as e:
        print(f"🚨 SQL SYNTAX ERROR: {e}")

def solve_ctf_case():
    """The automated verification engine that checks if the user solved the mystery."""
    print("\n--- 🏆 SUBMIT CTF FINAL REPORT ---")
    print("To close this investigation, you must identify the mole and their password.")
    
    suspect = input("Enter suspected mole's username (e.g., t_stark): ").strip().lower()
    password = input("Enter cracked plaintext password: ").strip()
    
    # Check against database ground truth
    try:
        query = "SELECT password_hash FROM credentials WHERE username = ?"
        results = execute_query(query, (suspect,))
        
        if not results:
            print("❌ REPORT REJECTED: Suspect username does not exist in corporate records!")
            return
            
        import hashlib
        entered_hash = hashlib.sha256(password.encode()).hexdigest()
        actual_hash = results[0][0]
        
        if entered_hash == actual_hash and suspect == "n_ryder":
            print("\n" + "🎉"*30)
            print(" 🚨 CASE SOLVED! YOU CAUGHT THE MOLE! 🚨 ")
            print("🎉"*30)
            print(f"Nyx Ryder ({suspect}) used an external IP to exfiltrate 'project_icarus_core.zip'")
            print("using the dictionary-vulnerable password: '{}'".format(password))
            print("NexusCorp security has locked down the network. Outstanding work, Detective!")
            print("🎉"*30 + "\n")
        else:
            print("❌ REPORT REJECTED: Incorrect username or password combination. Keep investigating!")
            
    except Exception as e:
        print(f"🚨 Error verifying report: {e}")

def main():
    """Main terminal loop."""
    print("⚡ Booting Nexus-OS Core...")
    time.sleep(0.5)
    
    # Automatically initialize clean database on startup
    initialize_db()
    
    while True:
        print_header()
        print("1. 🔌 Reset / Re-Initialize Crime Scene Database")
        print("2. 🌐 Run Regex Scanner: Detect Intruder IPs & Stolen Files")
        print("3. 📧 Run Regex Scanner: Audit Staff Email Formatting")
        print("4. 🔓 Launch SHA-256 Dictionary Attack (Crack a User Account)")
        print("5. 🛡️ Run Full Company Credential Security Audit")
        print("6. 💻 Open Direct SQL Query Console")
        print("7. 🏆 Submit Final Case Report (Solve CTF)")
        print("8. 🚪 Exit Terminal")
        
        choice = input("\nEnter terminal command (1-8): ").strip()
        
        if choice == "1":
            print("\n⚠️ Wiping corrupted logs and re-seeding database...")
            initialize_db()
            input("\nPress Enter to continue...")
        elif choice == "2":
            scan_for_ips()
            scan_for_exfiltrated_files()
            input("\nPress Enter to return to terminal...")
        elif choice == "3":
            scan_employee_emails()
            input("\nPress Enter to return to terminal...")
        elif choice == "4":
            print("\n--- 🔓 SHA-256 PASSWORD CRACKER ---")
            target = input("Enter target username to crack (e.g., n_ryder): ").strip().lower()
            if target:
                crack_password(target)
            else:
                print("❌ Username cannot be empty!")
            input("\nPress Enter to return to terminal...")
        elif choice == "5":
            audit_all_passwords()
            input("\nPress Enter to return to terminal...")
        elif choice == "6":
            run_custom_sql_query()
            input("\nPress Enter to return to terminal...")
        elif choice == "7":
            solve_ctf_case()
            input("\nPress Enter to return to terminal...")
        elif choice == "8":
            print("\n👋 Logging out of Nexus-OS Forensic Terminal. Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid command! Please select an option from 1 to 8.")

if __name__ == "__main__":
    main()