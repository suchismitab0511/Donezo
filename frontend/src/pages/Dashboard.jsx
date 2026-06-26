import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../api/axios";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await api.get("/api/tasks/");
      setTasks(res.data);
    } catch (err) {
      setError("Failed to load tasks.");
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score >= 7) return "bg-red-100 text-red-700 border-red-200";
    if (score >= 4) return "bg-amber-100 text-amber-700 border-amber-200";
    return "bg-green-100 text-green-700 border-green-200";
  };

  const getRiskLabel = (score) => {
    if (score >= 7) return "High Risk";
    if (score >= 4) return "Medium Risk";
    return "Low Risk";
  };

  const formatDeadline = (deadline) => {
    const date = new Date(deadline);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
            <p className="text-gray-500 text-sm mt-1">
              {tasks.length} task{tasks.length !== 1 ? "s" : ""} active
            </p>
          </div>
          <button
            onClick={() => navigate("/tasks/new")}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-4 py-2 rounded-xl transition text-sm"
          >
            + New Task
          </button>
        </div>

        {loading && (
          <div className="text-center text-gray-400 py-20">Loading tasks...</div>
        )}

        {error && (
          <div className="text-center text-red-500 py-20">{error}</div>
        )}

        {!loading && !error && tasks.length === 0 && (
          <div className="text-center py-20">
            <p className="text-4xl mb-3">📋</p>
            <p className="text-gray-500 font-medium">No tasks yet.</p>
            <p className="text-gray-400 text-sm mt-1">
              Add your first task and let AI break it down.
            </p>
          </div>
        )}

        <div className="flex flex-col gap-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              onClick={() => navigate(`/tasks/${task.id}`)}
              className="bg-white border border-gray-200 rounded-2xl px-5 py-4 cursor-pointer hover:shadow-md transition"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1">
                  <h2 className="text-gray-900 font-semibold text-base">
                    {task.title}
                  </h2>
                  <p className="text-gray-400 text-sm mt-1">
                    Due {formatDeadline(task.deadline)}
                  </p>
                </div>
                {task.risk_score !== null && (
                  <span
                    className={`text-xs font-semibold px-3 py-1 rounded-full border ${getRiskColor(
                      task.risk_score
                    )}`}
                  >
                    {getRiskLabel(task.risk_score)}
                  </span>
                )}
              </div>

              <div className="mt-3 flex items-center gap-2">
                <span
                  className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    task.status === "completed"
                      ? "bg-green-100 text-green-700"
                      : task.status === "in_progress"
                      ? "bg-blue-100 text-blue-700"
                      : "bg-gray-100 text-gray-500"
                  }`}
                >
                  {task.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}