from .database import (
    get_exams,
    get_teachers,
    update_exam_teacher,
    log_action,
)

def get_exam_schedule():
    """Returns the current exam schedule."""

    return {
        "success": True,
        "exams": get_exams(),
    }


def get_teacher_availability():
    """Returns teacher availability from the school database."""

    teachers = get_teachers()

    return {
        "teachers": teachers
    }
def check_teacher_conflict(teacher_name: str, exam_time: str):
    """Checks the actual exam database for teacher conflicts."""

    exams = get_exams()

    conflicts = [
        exam
        for exam in exams
        if exam["teacher"] == teacher_name
        and exam["time"] == exam_time
    ]

    if conflicts:
        return {
            "teacher": teacher_name,
            "time": exam_time,
            "has_conflict": True,
            "conflicts": conflicts,
            "message": (
                f"{teacher_name} already has an exam assignment "
                f"at {exam_time}."
            ),
        }

    return {
        "teacher": teacher_name,
        "time": exam_time,
        "has_conflict": False,
        "conflicts": [],
        "message": (
            f"{teacher_name} has no exam conflict at {exam_time}."
        ),
    }


def update_exam_schedule(
    exam_id: int,
    replacement_teacher: str,
    reason: str = "Replacement required due to teacher absence",
):
    """Safely updates an exam supervisor after checking for conflicts."""

    exams = get_exams()

    exam = next(
        (exam for exam in exams if exam["id"] == exam_id),
        None
    )

    if exam is None:
        return {
            "success": False,
            "message": f"Exam with ID {exam_id} was not found."
        }

    exam_time = exam["time"]
    old_teacher = exam["teacher"]

    # SAFETY CHECK: never assign a teacher who has a conflict
    conflict = check_teacher_conflict(
        replacement_teacher,
        exam_time
    )

    if conflict["has_conflict"]:
        return {
            "success": False,
            "message": (
                f"Cannot assign {replacement_teacher}. "
                f"They have a scheduling conflict at {exam_time}."
            ),
            "exam_id": exam_id,
            "teacher": replacement_teacher,
            "exam_time": exam_time,
            "conflicts": conflict["conflicts"],
        }

    if old_teacher == replacement_teacher:
        return {
            "success": False,
            "message": (
                f"{replacement_teacher} is already assigned "
                f"to exam {exam_id}."
            )
        }

    success = update_exam_teacher(
        exam_id,
        replacement_teacher
    )

    if not success:
        return {
            "success": False,
            "message": "Database update failed."
        }

    log_action(
        exam_id=exam_id,
        action="REPLACEMENT_TEACHER_ASSIGNED",
        old_teacher=old_teacher,
        new_teacher=replacement_teacher,
        reason=reason,
    )

    # VERIFY after update
    updated_exams = get_exams()

    updated_exam = next(
        (e for e in updated_exams if e["id"] == exam_id),
        None
    )

    verified = (
        updated_exam is not None
        and updated_exam["teacher"] == replacement_teacher
    )

    if not verified:
        return {
            "success": False,
            "message": "Update could not be verified."
        }

    return {
        "success": True,
        "message": "Exam schedule updated, logged, and verified.",
        "exam_id": exam_id,
        "old_teacher": old_teacher,
        "new_teacher": replacement_teacher,
        "exam_time": exam_time,
        "reason": reason,
        "verified": True,
    }

def run_schoolops_workflow(absent_teacher: str = "Ahmed"):
    """
    Runs the SchoolOps exam replacement workflow.

    Finds the exam assigned to the absent teacher,
    selects the best available replacement,
    safely updates the database, and verifies the result.
    """

    exams = get_exams()
    teachers = get_teachers()

    # 1. Find the affected exam
    affected_exam = next(
        (
            exam
            for exam in exams
            if exam["teacher"].lower() == absent_teacher.lower()
        ),
        None,
    )

    if affected_exam is None:
        return {
            "success": False,
            "message": f"No exam found for {absent_teacher}.",
        }

    exam_id = affected_exam["id"]
    exam_time = affected_exam["time"]

    # 2. Find suitable replacement teachers
    candidates = []

    for teacher in teachers:

        if teacher["status"] != "Available":
            continue

        if exam_time not in teacher["available_times"]:
            continue

        # 3. Check actual database conflicts
        conflict = check_teacher_conflict(
            teacher["name"],
            exam_time,
        )

        if conflict["has_conflict"]:
            continue

        candidates.append(
            {
                "name": teacher["name"],
                "availability_count": len(
                    teacher["available_times"]
                ),
            }
        )

    if not candidates:
        return {
            "success": False,
            "message": (
                f"No suitable replacement teacher was found "
                f"for {exam_time}."
            ),
            "exam": affected_exam,
        }

    # 4. Greatest availability wins
    candidates.sort(
        key=lambda teacher: teacher["availability_count"],
        reverse=True,
    )

    selected_teacher = candidates[0]["name"]

    # 5. Update database safely
    result = update_exam_schedule(
        exam_id,
        selected_teacher,
        (
            f"{absent_teacher} is absent tomorrow. "
            "Selected the teacher with the greatest "
            "availability and no scheduling conflict."
        ),
    )

    if not result["success"]:
        return result

    # 6. Verify database
    updated_exams = get_exams()

    updated_exam = next(
        (
            exam
            for exam in updated_exams
            if exam["id"] == exam_id
        ),
        None,
    )

    verified = (
        updated_exam is not None
        and updated_exam["teacher"] == selected_teacher
    )

    if not verified:
        return {
            "success": False,
            "message": "Database update could not be verified.",
        }

    return {
        "success": True,
        "message": "SchoolOps workflow completed successfully.",
        "exam": updated_exam,
        "selected_teacher": selected_teacher,
        "candidates": candidates,
        "verified": True,
    }