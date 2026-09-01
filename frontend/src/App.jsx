
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [request, setRequest] = useState("");
  const [activity, setActivity] = useState([]);
  const [isRunning, setIsRunning] = useState(false);

  const [exams, setExams] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [examResponse, teacherResponse, auditResponse] =
        await Promise.all([
          fetch("http://127.0.0.1:8000/api/exams"),
          fetch("http://127.0.0.1:8000/api/teachers"),
          fetch("http://127.0.0.1:8000/api/audit-logs"),
        ]);

      const examData = await examResponse.json();
      const teacherData = await teacherResponse.json();
      const auditData = await auditResponse.json();

      setExams(examData.exams || []);
      setTeachers(teacherData.teachers || []);
      setAuditLogs(auditData.logs || []);
    } catch (error) {
      console.error("Failed to load SchoolOps data:", error);
      setMessage("Failed to connect to SchoolOps backend.");
    }
  };

 const runAgent = async () => {
  if (!request.trim()) {
    setMessage("⚠️ Please enter an operational request.");
    return;
  }

  setIsRunning(true);
  setMessage("");

  // Show the actual workflow stages while the request is processing
  setActivity([
    "🔎 Inspecting exam schedule...",
    "👩‍🏫 Checking teacher availability...",
    "🔍 Checking scheduling conflicts...",
    "🧠 Selecting the best replacement...",
  ]);

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/run-workflow?request=${encodeURIComponent(
        request
      )}`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (data.success) {
      const selectedTeacher = data.selected_teacher;
      const candidateCount = data.candidates
        ? data.candidates.length
        : 0;

      setActivity([
        `🔎 Exam identified: ${data.exam.subject} — ${data.exam.time}`,
        `👩‍🏫 Found ${candidateCount} available replacement candidates`,
        "🔍 Checked scheduling conflicts",
        `🧠 Selected ${selectedTeacher} based on availability and conflict checks`,
        "💾 Updating exam database...",
        "📋 Recording action in audit log...",
        "✅ Database update verified successfully",
      ]);

      setMessage(
        `✅ Exam ${data.exam.id} updated successfully. New supervisor: ${selectedTeacher}.`
      );

      await loadData();
    } else {
      setActivity((prev) => [
        ...prev,
        `❌ ${data.message}`,
      ]);

      setMessage(`❌ ${data.message}`);
    }
  } catch (error) {
    console.error("Workflow error:", error);

    setMessage("❌ Could not connect to SchoolOps backend.");

    setActivity((prev) => [
      ...prev,
      "❌ Backend connection failed.",
    ]);
  } finally {
    setIsRunning(false);
  }
};

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>SchoolOps</h1>
          <p>AI School Operations Manager</p>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Agent Online
        </div>
      </header>

      <main>
        <section className="hero">
          <div>
            <h2>Autonomous School Operations</h2>

            <p>
              Let SchoolOps analyze operational problems, make decisions,
              execute actions, and verify the results.
            </p>
          </div>
        </section>

        <section className="agent-card">
          <h2>🤖 Ask SchoolOps Agent</h2>

          <textarea
            value={request}
            onChange={(e) => setRequest(e.target.value)}
            placeholder="Example: Ahmed is absent tomorrow. Find the best replacement for his exam."
          />

          <button onClick={runAgent} disabled={isRunning}>
            {isRunning
              ? "SchoolOps Agent is working..."
              : "Run SchoolOps Agent"}
          </button>

          {message && (
            <p className="agent-message">{message}</p>
          )}

          {activity.length > 0 && (
            <div className="activity-panel">
              <h3>🤖 Agent Activity</h3>

              <div className="activity-list">
                {activity.map((step, index) => (
                  <div className="activity-step" key={index}>
                    <span className="activity-number">
                      {index + 1}
                    </span>

                    <span>{step}</span>
                  </div>
                ))}
              </div>

              {isRunning && (
                <p className="activity-running">
                  🤖 SchoolOps Agent is working...
                </p>
              )}
            </div>
          )}
        </section>

        <section className="section">
          <h2>📅 Exam Schedule</h2>

          <div className="table-card">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Grade</th>
                  <th>Subject</th>
                  <th>Teacher</th>
                  <th>Room</th>
                  <th>Time</th>
                </tr>
              </thead>

              <tbody>
                {exams.map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.id}</td>
                    <td>{exam.grade}</td>
                    <td>{exam.subject}</td>
                    <td>{exam.teacher}</td>
                    <td>{exam.room}</td>
                    <td>{exam.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="section">
          <h2>👩‍🏫 Teacher Availability</h2>

          <div className="teacher-grid">
            {teachers.map((teacher) => (
              <div className="teacher-card" key={teacher.name}>
                <h3>{teacher.name}</h3>

                <p>
                  Status:{" "}
                  <strong
                    className={
                      teacher.status === "Available"
                        ? "available"
                        : "absent"
                    }
                  >
                    {teacher.status}
                  </strong>
                </p>

                <p>
                  Available:{" "}
                  {teacher.available_times &&
                  teacher.available_times.length > 0
                    ? teacher.available_times.join(", ")
                    : "None"}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="section">
          <h2>⚡ Agent Workflow</h2>

          <div className="workflow">
            <div>1. Inspect Schedule</div>
            <div>2. Find Available Teachers</div>
            <div>3. Check Conflicts</div>
            <div>4. Select Best Replacement</div>
            <div>5. Update Database</div>
            <div>6. Verify Result</div>
          </div>
        </section>

        <section className="section">
          <h2>📋 Audit Log</h2>

          <div className="table-card">
            <table>
              <thead>
                <tr>
                  <th>Action</th>
                  <th>Exam</th>
                  <th>Previous Teacher</th>
                  <th>New Teacher</th>
                  <th>Reason</th>
                  <th>Time</th>
                </tr>
              </thead>

              <tbody>
                {auditLogs.length === 0 ? (
                  <tr>
                    <td colSpan="6">
                      No actions recorded yet.
                    </td>
                  </tr>
                ) : (
                  auditLogs.map((log) => (
                    <tr key={log.id}>
                      <td>{log.action}</td>
                      <td>{log.exam_id}</td>
                      <td>{log.old_teacher}</td>
                      <td>{log.new_teacher}</td>
                      <td>{log.reason}</td>
                      <td>{log.created_at}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;

