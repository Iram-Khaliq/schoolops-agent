import sqlite3
from pathlib import Path


DATABASE_NAME = Path(__file__).resolve().parent / "schoolops.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Exams table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grade TEXT NOT NULL,
            subject TEXT NOT NULL,
            teacher TEXT NOT NULL,
            room TEXT NOT NULL,
            exam_time TEXT NOT NULL
        )
    """)

    # Add sample exams only if table is empty
    cursor.execute("SELECT COUNT(*) FROM exams")

    if cursor.fetchone()[0] == 0:
        exams = [
            ("Grade 8", "English", "Ahmed", "Room 4", "09:00"),
            ("Grade 8", "Mathematics", "Sara", "Room 2", "11:00"),
            ("Grade 8", "Science", "Ali", "Room 3", "13:00"),
        ]

        cursor.executemany("""
            INSERT INTO exams
            (grade, subject, teacher, room, exam_time)
            VALUES (?, ?, ?, ?, ?)
        """, exams)

    # Teachers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            available_times TEXT NOT NULL
        )
    """)

    # Add sample teachers only if table is empty
    cursor.execute("SELECT COUNT(*) FROM teachers")

    if cursor.fetchone()[0] == 0:
        teachers = [
            ("Ahmed", "Absent", ""),
            ("Sara", "Available", "09:00"),
            ("Ali", "Available", "09:00"),
            ("Fatima", "Available", "09:00,11:00"),
        ]

        cursor.executemany("""
            INSERT INTO teachers
            (name, status, available_times)
            VALUES (?, ?, ?)
        """, teachers)

    # Audit logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            old_teacher TEXT,
            new_teacher TEXT,
            reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def get_exams():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, grade, subject, teacher, room, exam_time
        FROM exams
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row[0],
            "grade": row[1],
            "subject": row[2],
            "teacher": row[3],
            "room": row[4],
            "time": row[5],
        }
        for row in rows
    ]


def update_exam_teacher(exam_id: int, teacher_name: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE exams
        SET teacher = ?
        WHERE id = ?
    """, (teacher_name, exam_id))

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


def log_action(
    exam_id: int,
    action: str,
    old_teacher: str,
    new_teacher: str,
    reason: str,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_logs
        (exam_id, action, old_teacher, new_teacher, reason)
        VALUES (?, ?, ?, ?, ?)
    """, (
        exam_id,
        action,
        old_teacher,
        new_teacher,
        reason
    ))

    connection.commit()
    connection.close()


def get_audit_logs():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            exam_id,
            action,
            old_teacher,
            new_teacher,
            reason,
            created_at
        FROM audit_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row[0],
            "exam_id": row[1],
            "action": row[2],
            "old_teacher": row[3],
            "new_teacher": row[4],
            "reason": row[5],
            "created_at": row[6],
        }
        for row in rows
    ]


def get_teachers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, status, available_times
        FROM teachers
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "status": row[2],
            "available_times": (
                row[3].split(",") if row[3] else []
            ),
        }
        for row in rows
    ]

def clear_audit_logs():
    """Clear audit logs during development/demo preparation."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM audit_logs")

    connection.commit()
    connection.close()