import sqlite3
import os

# Define the database file path
db_path = os.path.join(os.getcwd(), 'sqlite_db', 'finance.db')

# Ensure the directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    weight INTEGER,
    height INTEGER
)
''')

# Create the dailyactivity table
c.execute('''
CREATE TABLE IF NOT EXISTS dailyactivity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steps INTEGER,
    food TEXT,
    jog INTEGER,
    sleep INTEGER,
    user TEXT,
    calories INTEGER,
    FOREIGN KEY(user) REFERENCES users(username)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
print("Database and tables created successfully.")