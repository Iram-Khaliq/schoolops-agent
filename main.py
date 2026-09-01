from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from .agent import root_agent

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
)


app = FastAPI(
    title="SchoolOps API",
    description="API for the SchoolOps autonomous school operations manager",
)

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="schoolops",
    session_service=session_service,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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