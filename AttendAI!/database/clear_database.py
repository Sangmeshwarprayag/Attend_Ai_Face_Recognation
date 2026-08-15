import sqlite3

conn = sqlite3.connect("database/attendai.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM attendance")
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM subjects")
cursor.execute("DELETE FROM lectures")
cursor.execute("DELETE FROM users")

conn.commit()
conn.close()

print("All database data deleted successfully")
