import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_FILE = Path("study_records.db")
def get_recent_records(days=7):
    start_date = date.today() - timedelta(days=days - 1)

    connection = get_connection()
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            study_date,
            subject,
            duration_minutes,
            python_level,
            note
        FROM study_records
        WHERE study_date >= ?
        ORDER BY study_date DESC, id DESC
        """,
        (str(start_date),),
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]
def get_recent_summary(days=7):
    records = get_recent_records(days)

    total_minutes = sum(
        record["duration_minutes"]
        for record in records
    )

    subject_minutes = {}

    for record in records:
        subject = record["subject"]
        subject_minutes[subject] = (
            subject_minutes.get(subject, 0)
            + record["duration_minutes"]
        )

    return {
        "records": records,
        "total_minutes": total_minutes,
        "subject_minutes": subject_minutes,
    }

def get_connection():
    return sqlite3.connect(DB_FILE)


def initialize_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS study_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_date TEXT NOT NULL,
            subject TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            python_level TEXT NOT NULL,
            note TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()
def add_record(study_date, subject, duration_minutes, python_level, note):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO study_records (
            study_date,
            subject,
            duration_minutes,
            python_level,
            note
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            study_date,
            subject,
            duration_minutes,
            python_level,
            note,
        ),
    )

    connection.commit()
    connection.close()
def get_records():
    connection = get_connection()
    connection.row_factory = sqlite3.Row

    rows = connection.execute(
        """
        SELECT
            study_date AS 日期,
            subject AS 学习主题,
            duration_minutes AS 学习时长（分钟）,
            python_level AS Python基础,
            note AS 学习心得
        FROM study_records
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
def record_exists(study_date, subject, duration_minutes, python_level, note):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT 1
        FROM study_records
        WHERE study_date = ?
          AND subject = ?
          AND duration_minutes = ?
          AND python_level = ?
          AND note = ?
        LIMIT 1
        """,
        (
            study_date,
            subject,
            duration_minutes,
            python_level,
            note,
        ),
    ).fetchone()

    connection.close()
    return row is not None