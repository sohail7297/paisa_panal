import sqlite3
import hashlib

DB_NAME = "users.db"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def add_admin(username, password, email="", phone=""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, hashed_password, email, phone, role) VALUES (?, ?, ?, ?, 'admin')",
                  (username, hashed, email, phone))
        conn.commit()
        print(f"Admin user '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists!")
    finally:
        conn.close()

if __name__ == "__main__":
    add_admin("sohail7297", "sohail0852")
