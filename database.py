
import sqlite3

DB_NAME = "job_tracker.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            job_role TEXT NOT NULL,
            location TEXT,
            application_date TEXT,
            status TEXT DEFAULT 'Applied',
            interview_date TEXT,
            job_link TEXT
        )
    """)

    conn.commit()
    conn.close()
