import sqlite3

conn = sqlite3.connect("workflows.db")
cursor = conn.cursor()

columns = [
    ("current_interest", "REAL"),
    ("average_interest", "REAL"),
    ("growth_percent", "REAL"),
    ("interest_score", "REAL"),
    ("average_score", "REAL"),
    ("growth_score", "REAL"),
    ("overall_score", "REAL"),
]

for name, data_type in columns:
    try:
        cursor.execute(
            f"ALTER TABLE workflows ADD COLUMN {name} {data_type}"
        )
        print(f"Added: {name}")
    except sqlite3.OperationalError:
        print(f"Already exists: {name}")

conn.commit()
conn.close()

print("Migration completed.")