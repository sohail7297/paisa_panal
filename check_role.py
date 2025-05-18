import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("SELECT username, role FROM users WHERE username = ?", ("sohail7297",))
user = c.fetchone()
conn.close()

print(user)
