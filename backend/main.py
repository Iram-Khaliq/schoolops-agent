from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import (
    initialize_database,
    get_exams,
    get_teachers,
    get_audit_logs,
)

from .tools import (
    get_exam_schedule,
    get_teacher_availability,
    check_teacher_conflict,
    update_exam_schedule,
    run_schoolops_workflow,
)

app = FastAPI(
    title="SchoolOps API",
    description="API for the SchoolOps autonomous school operations manager",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


initialize_database()


@app.get("/")
def root():
    return {
        "message": "SchoolOps API is running"
    }


@app.get("/api/exams")
def exams():
    return get_exam_schedule()


@app.get("/api/teachers")
def teachers():
    return get_teacher_availability()


@app.get("/api/audit-logs")
def audit_logs():
    return {
        "logs": get_audit_logs()
    }


@app.post("/api/update-exam")
def update_exam(
    exam_id: int,
    replacement_teacher: str,
    reason: str = "Replacement required due to teacher absence",
):
    return update_exam_schedule(
        exam_id,
        replacement_teacher,
        reason,
    )


@app.post("/api/run-workflow")
def run_workflow(request: str):
    """
    Runs SchoolOps based on the user's operational request.
    """

    request_lower = request.lower()

    if "ahmed" in request_lower:
        absent_teacher = "Ahmed"
    elif "sara" in request_lower:
        absent_teacher = "Sara"
    elif "ali" in request_lower:
        absent_teacher = "Ali"
    elif "fatima" in request_lower:
        absent_teacher = "Fatima"
    else:
        return {
            "success": False,
            "message": "Could not identify the absent teacher from the request.",
        }

    return run_schoolops_workflow(absent_teacher)