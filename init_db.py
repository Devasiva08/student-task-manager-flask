import sqlite3

conn = sqlite3.connect("tasks.db")
conn.execute("""
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
""")
conn.commit()
conn.close()
print("Database created")
