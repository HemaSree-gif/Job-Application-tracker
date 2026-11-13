
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "job_tracker.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    cursor.execute("BEGIN TRANSACTION")

    cursor.execute("SELECT id FROM applications ORDER BY id ASC")
    records = cursor.fetchall()

    # Temporarily move existing IDs to negative values
    for (old_id,) in records:
        cursor.execute(
            "UPDATE applications SET id = ? WHERE id = ?",
            (-old_id, old_id)
        )

    # Assign new IDs starting from 1
    for new_id, (old_id,) in enumerate(records, start=1):
        cursor.execute(
            "UPDATE applications SET id = ? WHERE id = ?",
            (new_id, -old_id)
        )

    # Reset SQLite's automatic ID counter
    cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name = 'applications'"
    )

    if records:
        cursor.execute(
            "INSERT INTO sqlite_sequence (name, seq) VALUES (?, ?)",
            ("applications", len(records))
        )

    conn.commit()
    print("Application IDs successfully reset!")

    cursor.execute(
        "SELECT id, company_name FROM applications ORDER BY id ASC"
    )

    for record in cursor.fetchall():
        print(record)

except Exception as error:
    conn.rollback()
    print("Error:", error)

finally:
    conn.close()