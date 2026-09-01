from google.cloud import firestore


# Google Cloud / Firestore project
PROJECT_ID = "schoolop"

# Firestore client
db = firestore.Client(project=PROJECT_ID)


# Firestore collection names
EXAMS_COLLECTION = "exams"
TEACHERS_COLLECTION = "teachers"
AUDIT_LOGS_COLLECTION = "audit_logs"


# ---------------------------------------------------------
# EXAMS
# ---------------------------------------------------------

def get_exams():
    """Return all exams from Firestore."""

    docs = (
        db.collection(EXAMS_COLLECTION)
        .stream()
    )

    exams = []

    # Map Firestore document IDs to stable numeric IDs
    # so the existing tools.py continues to work.
    id_map = {
        "grade8_english": 1,
        "grade8_math": 2,
        "grade8_science": 3,
    }

    for doc in docs:
        data = doc.to_dict()

        exams.append({
            "id": id_map.get(doc.id, doc.id),
            "grade": data.get("grade", ""),
            "subject": data.get("subject", ""),
            "teacher": data.get("teacher", ""),
            "room": data.get("room", ""),
            "time": data.get("time", ""),
        })

    return exams


def update_exam_teacher(exam_id: int, teacher_name: str):
    """Update the teacher assigned to an exam in Firestore."""

    id_map = {
        1: "grade8_english",
        2: "grade8_math",
        3: "grade8_science",
    }

    document_id = id_map.get(exam_id)

    if document_id is None:
        return False

    exam_ref = db.collection(EXAMS_COLLECTION).document(
        document_id
    )

    snapshot = exam_ref.get()

    if not snapshot.exists:
        return False

    exam_ref.update({
        "teacher": teacher_name
    })

    return True


# ---------------------------------------------------------
# TEACHERS
# ---------------------------------------------------------

def get_teachers():
    """Return teachers from Firestore."""

    docs = (
        db.collection(TEACHERS_COLLECTION)
        .stream()
    )

    teachers = []

    id_map = {
        "ahmed": 1,
        "sara": 2,
        "ali": 3,
        "fatima": 4,
    }

    for doc in docs:
        data = doc.to_dict()

        available_times = data.get(
            "available_times",
            []
        )

        # Handle Firestore string or array values safely
        if isinstance(available_times, str):
            available_times = (
                [available_times]
                if available_times.strip()
                else []
            )

        # Clean whitespace/newlines
        available_times = [
            str(time).strip()
            for time in available_times
            if str(time).strip()
        ]

        teachers.append({
            "id": id_map.get(doc.id, doc.id),
            "name": data.get("name", ""),
            "status": data.get(
                "status",
                "Unavailable"
            ),
            "available_times": available_times,
        })

    return teachers
# ---------------------------------------------------------
# AUDIT LOGS
# ---------------------------------------------------------

def log_action(
    exam_id: int,
    action: str,
    old_teacher: str,
    new_teacher: str,
    reason: str,
):
    """Write an audit log entry to Firestore."""

    db.collection(AUDIT_LOGS_COLLECTION).add({
        "exam_id": exam_id,
        "action": action,
        "old_teacher": old_teacher,
        "new_teacher": new_teacher,
        "reason": reason,
        "created_at": firestore.SERVER_TIMESTAMP,
    })


def get_audit_logs():
    """Return audit logs from Firestore."""

    docs = (
        db.collection(AUDIT_LOGS_COLLECTION)
        .order_by(
            "created_at",
            direction=firestore.Query.DESCENDING
        )
        .stream()
    )

    logs = []

    counter = 1

    for doc in docs:
        data = doc.to_dict()

        created_at = data.get("created_at")

        logs.append({
            "id": counter,
            "exam_id": data.get("exam_id"),
            "action": data.get("action"),
            "old_teacher": data.get("old_teacher"),
            "new_teacher": data.get("new_teacher"),
            "reason": data.get("reason"),
            "created_at": created_at,
        })

        counter += 1

    return logs


# ---------------------------------------------------------
# DEVELOPMENT HELPER
# ---------------------------------------------------------

def clear_audit_logs():
    """Clear all audit logs during development/demo preparation."""

    docs = (
        db.collection(AUDIT_LOGS_COLLECTION)
        .stream()
    )

    for doc in docs:
        doc.reference.delete()