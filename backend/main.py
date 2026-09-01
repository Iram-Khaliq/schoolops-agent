from dotenv import load_dotenv

load_dotenv(r"D:\schoolops-agent\backend\.env")
from google.genai import types
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from .agent import root_agent

from .database import (
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
session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="schoolops",
    session_service=session_service,
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

@app.post("/api/test-agent")
async def test_agent(request: str):
    """
    Runs the real SchoolOps ADK agent.

    If Gemini is unavailable or quota is exhausted,
    falls back to the local deterministic workflow.
    """

    user_id = "hackathon-demo-user"
    session_id = "schoolops-demo-session"

    try:
        session = await session_service.get_session(
            app_name="schoolops",
            user_id=user_id,
            session_id=session_id,
        )

        if session is None:
            session = await session_service.create_session(
                app_name="schoolops",
                user_id=user_id,
                session_id=session_id,
            )

        content = types.Content(
            role="user",
            parts=[
                types.Part(text=request)
            ],
        )

        events = []

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        events.append(part.text)

        return {
            "success": True,
            "mode": "adk",
            "agent_response": "\n".join(events),
        }

    except Exception as error:
        error_text = str(error)

        # Gemini quota / temporary API failure → local safety fallback
        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "503" in error_text
            or "UNAVAILABLE" in error_text
        ):
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
                    "mode": "fallback",
                    "message": (
                        "Gemini is temporarily unavailable and "
                        "the absent teacher could not be identified."
                    ),
                }

            result = run_schoolops_workflow(absent_teacher)

            result["mode"] = "local_fallback"
            result["agent_error"] = (
                "Gemini API temporarily unavailable; "
                "safety fallback executed."
            )

            return result

        return {
            "success": False,
            "mode": "adk",
            "error": error_text,
        }