import hashlib
import time
from database import execute_query

# A simulated cybersecurity wordlist of common corporate and tech passwords.
# In a real CTF or penetration test, you might load a file like 'rockyou.txt' containing millions of words!
CYBERPUNK_WORDLIST = [
    "123456",
    "password",
    "admin",
    "nexus2026",
    "ironman123",
    "destroyer",
    "skynet2029",
    "mrrobot",
    "cyberpunk",
    "shadowrun",  # Notice the mole's password is sitting right here!
    "matrix",
    "neuromancer",
    "wintermute",
    "project_icarus",
    "letmein123"
]

def get_sha256_hash(plaintext):
    """Converts a standard text string into its SHA-256 hexadecimal hash."""
    # .encode() converts the Python string (Unicode) into raw bytes, which hashlib requires
    return hashlib.sha256(plaintext.encode()).hexdigest()

def crack_password(target_username, wordlist=CYBERPUNK_WORDLIST):
    """
    Queries the database for a user's password hash and executes a dictionary attack
    by hashing words from our list until a match is found.
    """
    print(f"\n--- 🔓 INITIATING DICTIONARY ATTACK AGAINST: [{target_username}] ---")
    
    # 1. Fetch the target's encrypted hash from our SQLite database
    query = "SELECT password_hash, access_level FROM credentials WHERE username = ?"
    results = execute_query(query, (target_username,))
    
    if not results:
        print(f"❌ Error: User '{target_username}' not found in the credentials database!")
        return None
        
    target_hash, access_level = results[0]
    print(f"🎯 Target Encrypted Hash: {target_hash[:25]}... (Access Level: {access_level})")
    print("⚙️ Loading wordlist and computing hashes in memory...\n")
    
    time.sleep(1) # Brief pause for terminal drama!
    
    attempts = 0
    start_time = time.time()
    
    # 2. Loop through every word in our dictionary
    for word in wordlist:
        attempts += 1
        
        # Hash the current dictionary word
        computed_hash = get_sha256_hash(word)
        
        # Print live progress to the terminal
        print(f"  [{attempts:>02}] Testing: {word:<15} -> {computed_hash[:15]}...")
        
        # 3. Check for a hash collision (a perfect match!)
        if computed_hash == target_hash:
            elapsed_time = time.time() - start_time
            print("\n" + "="*60)
            print(" 💥 HASH COLLISION DETECTED! PASSWORD CRACKED! 💥 ")
            print("="*60)
            print(f"👤 Username:    {target_username}")
            print(f"🔑 Plaintext:   {word}")
            print(f"🛡️ Access Level: {access_level}")
            print(f"⚡ Time Taken:  {elapsed_time:.4f} seconds ({attempts} attempts)")
            print("="*60)
            return word
            
        time.sleep(0.05) # Tiny artificial delay just so your eyes can read the terminal output
        
    print("\n❌ DICTIONARY ATTACK FAILED! Password not found in wordlist.")
    return None

def audit_all_passwords():
    """
    Runs an automated security audit across the entire corporate credentials table
    to see how many employees are using weak passwords from our wordlist.
    """
    print("\n--- 🛡️ RUNNING CORPORATE CREDENTIAL SECURITY AUDIT ---")
    all_users = execute_query("SELECT username FROM credentials")
    
    cracked_count = 0
    for row in all_users:
        user = row[0]
        # We run silently without printing every single attempt
        query = "SELECT password_hash FROM credentials WHERE username = ?"
        target_hash = execute_query(query, (user,))[0][0]
        
        found = False
        for word in CYBERPUNK_WORDLIST:
            if get_sha256_hash(word) == target_hash:
                print(f"  🚨 WEAK PASSWORD FOUND: User '{user:<12}' is using password '{word}'!")
                cracked_count += 1
                found = True
                break
                
        if not found:
            print(f"  ✅ SECURE: User '{user:<12}' password withstood dictionary attack.")
            
    print(f"\n💡 AUDIT COMPLETE: {cracked_count} out of {len(all_users)} accounts are vulnerable!")

# --- TESTING OUR CRACKER ---
if __name__ == "__main__":
    print("🕵️‍♂️ BOOTING UP SHA-256 FORENSIC CRACKER...")
    
    # Launch attack against our suspected mole
    cracked_secret = crack_password("n_ryder")
    
    # Run a full company audit
    audit_all_passwords()