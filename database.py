import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

# STUDENT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# ATTENDANCE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT
)
""")

connection.commit()
connection.close()

print("Database Created Successfully")
