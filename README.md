\# 🏫 SchoolOps Agent



\### Autonomous AI Operations Manager for Schools



SchoolOps Agent is an AI-powered school operations system that helps administrators handle teacher absences and exam-supervision changes automatically.



When a teacher is absent, the agent can inspect the current exam schedule, check teacher availability, evaluate scheduling conflicts, select the best available replacement, update the exam assignment in Firestore, verify the change, and record an audit log.



The goal is to turn a manual school-operations task into a \*\*safe, verifiable, autonomous workflow\*\*.



\---



\## 🚀 What Problem Does SchoolOps Solve?



School administrators often need to react quickly when a teacher becomes unavailable.



A simple replacement process can involve:



1\. Finding the teacher's exam assignment.

2\. Checking which teachers are available.

3\. Checking whether those teachers already have another exam.

4\. Choosing the best replacement.

5\. Updating the schedule.

6\. Confirming that the update actually happened.

7\. Keeping a record of what changed and why.



Doing this manually can be time-consuming and can introduce scheduling mistakes.



SchoolOps Agent automates this workflow while keeping the final database operation controlled and verifiable.



\---



\# 🤖 How SchoolOps Works



Example request:



> \*\*"Ahmed is absent tomorrow."\*\*



The SchoolOps workflow:



```text

Administrator Request

&#x20;       │

&#x20;       ▼

&#x20;  SchoolOps Agent

&#x20;       │

&#x20;       ▼

Read Current Exam Schedule

&#x20;       │

&#x20;       ▼

Find Ahmed's Exam

&#x20;       │

&#x20;       ▼

Read Teacher Availability

&#x20;       │

&#x20;       ▼

Check Scheduling Conflicts

&#x20;       │

&#x20;       ▼

Select Best Replacement

&#x20;       │

&#x20;       ▼

Update Firestore

&#x20;       │

&#x20;       ▼

Verify Database Change

&#x20;       │

&#x20;       ▼

Create Audit Log

```



The system does not simply generate a recommendation.



It can \*\*actually update the exam assignment and verify the resulting database state\*\*.



\---



\# ✨ Key Features



\## 1. Autonomous Teacher Replacement



The system identifies the exam supervised by an absent teacher and searches for suitable replacements.



Example:



```text

Ahmed → Absent



Grade 8 English

09:00

Room 4

```



The system evaluates available teachers and selects the best valid candidate.



\---



\## 2. Availability-Based Selection



Teachers have availability information stored in Firestore.



Example:



```text

Fatima

Status: Available

Available:

09:00

11:00

```



The workflow considers the teacher's availability when selecting a replacement.



When multiple teachers are suitable, the current workflow prefers the teacher with the \*\*greatest availability\*\*.



\---



\## 3. Conflict Detection



Before assigning a replacement teacher, SchoolOps checks the current exam schedule.



A teacher who already has an exam at the required time is rejected.



This prevents assignments such as:



```text

Fatima

09:00 → Exam A



Fatima

09:00 → Exam B

```



\---



\## 4. Safe Database Updates



The replacement is not considered successful merely because an update command was executed.



The system:



1\. Finds the affected exam.

2\. Checks the replacement teacher.

3\. Performs the update.

4\. Reads the exam again.

5\. Verifies that the new teacher is actually assigned.



Only then does the workflow report success.



\---



\## 5. Audit Logging



Every successful replacement is recorded in Firestore.



Example:



```text

Action:

REPLACEMENT\_TEACHER\_ASSIGNED



Old Teacher:

Ahmed



New Teacher:

Fatima



Reason:

Ahmed is absent tomorrow. Selected the teacher

with the greatest availability and no scheduling conflict.

```



This provides a history of operational changes.



\---



\# 🧠 AI Agent



SchoolOps uses \*\*Google ADK\*\* with a Gemini model as the reasoning layer.



The agent has access to the following operational tools:



```text

get\_exam\_schedule

get\_teacher\_availability

check\_teacher\_conflict

update\_exam\_schedule

```



The agent's instructions require it to:



\* Inspect the real schedule.

\* Identify the affected exam.

\* Check teacher availability.

\* Check scheduling conflicts.

\* Select an appropriate replacement.

\* Use the actual exam ID.

\* Perform the database update.

\* Verify the updated schedule.

\* Never claim success unless the update succeeds.



This makes the AI agent operate as an \*\*action-oriented operations manager\*\*, rather than only a conversational chatbot.



\---



\# 🏗️ Architecture



```text

┌───────────────────────────────┐

│        React Frontend         │

│                               │

│  Schedule / Teachers / Agent  │

└───────────────┬───────────────┘

&#x20;               │

&#x20;               │ HTTP

&#x20;               ▼

┌───────────────────────────────┐

│        FastAPI Backend        │

│                               │

│   REST API + Agent Runner     │

└───────────────┬───────────────┘

&#x20;               │

&#x20;       ┌───────┴────────┐

&#x20;       │                │

&#x20;       ▼                ▼

┌───────────────┐  ┌───────────────┐

│ Google ADK /  │  │ SchoolOps     │

│ Gemini Agent  │  │ Tools         │

└───────────────┘  └───────┬───────┘

&#x20;                          │

&#x20;                          ▼

&#x20;                 ┌─────────────────┐

&#x20;                 │ Google Firestore│

&#x20;                 │                 │

&#x20;                 │ Exams           │

&#x20;                 │ Teachers        │

&#x20;                 │ Audit Logs      │

&#x20;                 └─────────────────┘

```



\---



\# 🛠️ Technology Stack



\### Frontend



\* React

\* Vite

\* JavaScript

\* CSS



\### Backend



\* Python

\* FastAPI

\* Uvicorn



\### AI



\* Google ADK

\* Gemini

\* Google GenAI SDK



\### Database



\* Google Cloud Firestore



\### Development



\* Git

\* GitHub

\* Python virtual environment



\---



\# 📁 Project Structure



```text

schoolops-agent/

│

├── backend/

│   ├── agent/

│   ├── agent.py

│   ├── database.py

│   ├── main.py

│   ├── tools.py

│   ├── .env

│   └── schoolops.db

│

├── frontend/

│   └── src/

│       └── App.jsx

│

├── docs/

│

├── tests/

│

├── main.py

├── .gitignore

└── README.md

```



> `.env`, virtual environments, Python cache files, and database files are excluded from Git using `.gitignore`.



\---



\# ☁️ Firestore Data Model



SchoolOps currently uses three main Firestore collections.



\## `teachers`



Example document:



```text

teachers/fatima

```



```json

{

&#x20; "name": "Fatima",

&#x20; "status": "Available",

&#x20; "available\_times": \[

&#x20;   "09:00",

&#x20;   "11:00"

&#x20; ]

}

```



Example teachers currently used by the project:



```text

Ahmed

Ali

Fatima

Sara

```



\---



\## `exams`



Example document:



```text

exams/grade8\_english

```



```json

{

&#x20; "grade": "Grade 8",

&#x20; "subject": "English",

&#x20; "teacher": "Ahmed",

&#x20; "room": "Room 4",

&#x20; "time": "09:00"

}

```



Current demonstration schedule:



| Grade   | Subject     | Teacher | Room   | Time  |

| ------- | ----------- | ------- | ------ | ----- |

| Grade 8 | English     | Ahmed   | Room 4 | 09:00 |

| Grade 8 | Mathematics | Sara    | Room 2 | 11:00 |

| Grade 8 | Science     | Ali     | Room 3 | 13:00 |



\---



\## `audit\_logs`



Successful operational changes are stored in:



```text

audit\_logs

```



Example:



```json

{

&#x20; "exam\_id": 1,

&#x20; "action": "REPLACEMENT\_TEACHER\_ASSIGNED",

&#x20; "old\_teacher": "Ahmed",

&#x20; "new\_teacher": "Fatima",

&#x20; "reason": "Ahmed is absent tomorrow. Selected the teacher with the greatest availability and no scheduling conflict.",

&#x20; "created\_at": "server timestamp"

}

```



\---



\# 🔐 Environment Variables



Create:



```text

backend/.env

```



Add your Gemini API key:



```env

GOOGLE\_API\_KEY=your\_gemini\_api\_key

```



Never commit the real API key.



The repository's `.gitignore` excludes:



```text

.env

venv/

\_\_pycache\_\_/

\*.pyc

\*.db

```



\---



\# 💻 Local Setup



\## 1. Clone the repository



```bash

git clone https://github.com/Iram-Khaliq/schoolops-agent.git

cd schoolops-agent

```



\---



\## 2. Create the Python environment



From the project root:



\### Windows PowerShell



```powershell

python -m venv backend\\venv

```



Activate it:



```powershell

.\\backend\\venv\\Scripts\\Activate.ps1

```



\---



\## 3. Install backend dependencies



Install the required packages used by the project.



For example:



```powershell

pip install fastapi uvicorn python-dotenv google-adk google-genai google-cloud-firestore

```



\---



\# ☁️ Google Cloud / Firestore Authentication



The project uses Google Application Default Credentials for Firestore.



After installing the Google Cloud CLI, authenticate:



```powershell

gcloud auth application-default login

```



Set the project:



```powershell

gcloud config set project schoolop

```



Verify:



```powershell

gcloud config get-value project

```



Expected:



```text

schoolop

```



The Firestore client is configured for the `schoolop` Google Cloud project.



\---



\# ▶️ Run the Backend



From:



```text

D:\\schoolops-agent

```



activate the environment:



```powershell

.\\backend\\venv\\Scripts\\Activate.ps1

```



Then start FastAPI:



```powershell

python -m uvicorn backend.main:app --reload

```



The API runs at:



```text

http://127.0.0.1:8000

```



\---



\# 🌐 API Endpoints



\## Health Check



```http

GET /

```



Returns:



```json

{

&#x20; "message": "SchoolOps API is running"

}

```



\---



\## Get Exam Schedule



```http

GET /api/exams

```



Returns the current Firestore exam schedule.



\---



\## Get Teacher Availability



```http

GET /api/teachers

```



Returns teachers and their availability.



\---



\## Get Audit Logs



```http

GET /api/audit-logs

```



Returns recorded operational changes.



\---



\## Update Exam



```http

POST /api/update-exam

```



Updates an exam supervisor after conflict validation.



\---



\## Run Local SchoolOps Workflow



```http

POST /api/run-workflow

```



Example request:



```text

Ahmed is absent tomorrow

```



The endpoint identifies the absent teacher and executes the deterministic SchoolOps workflow.



\---



\## Run AI Agent



```http

POST /api/test-agent

```



This endpoint sends the request through the Google ADK agent.



Example:



```text

Ahmed is absent tomorrow

```



The ADK agent can inspect the schedule, use its tools, perform the replacement, and report the result.



\---



\# 🧪 Testing the Workflow



With the backend running, test the AI agent from PowerShell:



```powershell

Invoke-RestMethod `

&#x20; -Uri "http://127.0.0.1:8000/api/test-agent?request=Ahmed%20is%20absent%20tomorrow" `

&#x20; -Method POST

```



A successful response contains:



```text

success : True

mode    : adk

```



The agent response describes the resulting schedule change.



\---



\# 🔎 Verify the Database



You can verify the exam assignment directly:



```powershell

python -c "from backend.database import get\_exams; import pprint; pprint.pp(get\_exams())"

```



Example successful result:



```text

Grade 8 English

Teacher: Fatima

Time: 09:00

```



The remaining schedule stays unchanged:



```text

Grade 8 Mathematics

Teacher: Sara

Time: 11:00



Grade 8 Science

Teacher: Ali

Time: 13:00

```



\---



\# 🧾 Verify the Audit Log



Run:



```powershell

python -c "from backend.database import get\_audit\_logs; import pprint; pprint.pp(get\_audit\_logs())"

```



You should see a record similar to:



```text

action:

REPLACEMENT\_TEACHER\_ASSIGNED



old\_teacher:

Ahmed



new\_teacher:

Fatima

```



\---



\# 🧠 Example Decision



Suppose Ahmed is absent for the 09:00 English exam.



Available teachers:



```text

Ali

Available: 09:00



Sara

Available: 09:00



Fatima

Available: 09:00, 11:00

```



The workflow checks:



```text

Ali

09:00 → no conflict



Sara

09:00 → no conflict



Fatima

09:00 → no conflict

```



All three are valid candidates.



The current selection strategy prefers the teacher with the greatest availability:



```text

Fatima → 2 available times

Ali    → 1 available time

Sara   → 1 available time

```



Therefore:



```text

Ahmed → Fatima

```



The database is then updated and verified.



\---



\# 🛡️ Safety and Verification



SchoolOps is designed around several important safeguards.



\### No invented schedules



The agent is instructed to use the database tools instead of inventing schedule information.



\### Conflict prevention



A teacher with a conflicting exam assignment is rejected.



\### Database-backed updates



The replacement is actually written to Firestore.



\### Post-update verification



The system reads the schedule again after the update.



\### Auditability



Successful changes are recorded in the audit log.



\### No false success



The system does not report a successful replacement unless the update succeeds and can be verified.



\---



\# 🔄 AI Failure Handling



The backend also contains a deterministic local workflow.



This provides a useful fallback architecture:



```text

&#x20;                   User Request

&#x20;                        │

&#x20;                        ▼

&#x20;                 Google ADK Agent

&#x20;                        │

&#x20;                 ┌──────┴──────┐

&#x20;                 │             │

&#x20;             Available      API/Quota

&#x20;               │             Failure

&#x20;               ▼                │

&#x20;         AI Workflow            ▼

&#x20;                          Local Workflow

&#x20;                               │

&#x20;                               ▼

&#x20;                        Firestore Update

```



This allows the core scheduling operation to remain deterministic even when the Gemini service is temporarily unavailable.



\---



\# 🎯 Why This Is an Agent



SchoolOps is designed around an agentic workflow rather than a simple question-answering chatbot.



The agent can:



```text

Observe

&#x20;  ↓

Reason

&#x20;  ↓

Choose

&#x20;  ↓

Act

&#x20;  ↓

Verify

&#x20;  ↓

Report

```



For example:



```text

Observe:

Ahmed is absent.



Reason:

Ahmed supervises the 09:00 English exam.



Observe:

Fatima, Ali and Sara are available.



Reason:

Check their scheduling conflicts.



Choose:

Fatima has the greatest availability.



Act:

Update the exam assignment.



Verify:

Read the database again.



Report:

Ahmed was replaced by Fatima.

```



\---



\# 🏆 Hackathon Value



SchoolOps demonstrates several important AI-agent capabilities:



\* Autonomous multi-step reasoning

\* Tool calling

\* Real database interaction

\* Constraint-based decision making

\* Conflict detection

\* Persistent state

\* Action execution

\* Post-action verification

\* Auditability

\* Graceful fallback behavior



The important distinction is that the agent is not only generating text.



It can \*\*take an operational action and verify the resulting state\*\*.



\---



\# 📊 Current Project Status



| Component             | Status        |

| --------------------- | ------------- |

| React frontend        | ✅ Working     |

| FastAPI backend       | ✅ Working     |

| Google ADK agent      | ✅ Working     |

| Gemini integration    | ✅ Tested      |

| Firestore             | ✅ Connected   |

| Teacher collection    | ✅ Working     |

| Exam collection       | ✅ Working     |

| Conflict detection    | ✅ Working     |

| Automatic replacement | ✅ Working     |

| Database verification | ✅ Working     |

| Audit logging         | ✅ Working     |

| Git/GitHub            | ✅ Configured  |

| Cloud Run deployment  | ⏳ Future step |



\---



\# 🔮 Future Improvements



Possible next steps include:



\### Multi-exam optimization



Handle multiple absent teachers and optimize the complete exam schedule.



\### Better constraint solving



Consider:



\* Teacher subject expertise

\* Grade preferences

\* Room restrictions

\* Maximum supervision load

\* Teacher availability windows



\### Authentication



Add administrator authentication and role-based access.



\### Richer audit history



Provide filtering and reporting for historical scheduling changes.



\### Notifications



Notify administrators and teachers when a replacement is assigned.



\### Production deployment



Deploy the backend and frontend to production infrastructure.



\### Persistent agent sessions



Move beyond the current demo session handling toward persistent operational conversations.



\---



\# 📸 Demo



Recommended demonstration flow:



```text

1\. Open SchoolOps frontend

&#x20;            ↓

2\. Show current exam schedule

&#x20;            ↓

3\. Ask:

&#x20;  "Ahmed is absent tomorrow."

&#x20;            ↓

4\. Agent inspects schedule

&#x20;            ↓

5\. Agent checks teacher availability

&#x20;            ↓

6\. Agent checks conflicts

&#x20;            ↓

7\. Agent selects Fatima

&#x20;            ↓

8\. Firestore is updated

&#x20;            ↓

9\. Agent verifies the assignment

&#x20;            ↓

10\. Audit log is created

```



Expected result:



```text

Grade 8 English

09:00

Ahmed → Fatima

```



\---



\# 🔗 Repository



GitHub:



\*\*Iram-Khaliq/schoolops-agent\*\*



\---



\# 👩‍💻 Author



\*\*Iram Khaliq\*\*



Software Engineer focused on building practical AI-powered applications and autonomous workflows.



\---



\# 📄 License



This project is currently intended as a hackathon/demo project.



A production license can be added when the project is prepared for public distribution.



