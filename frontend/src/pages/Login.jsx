import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

export default function Login() {
  const { user, loginWithGoogle } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (user) navigate("/dashboard");
  }, [user]);

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 border border-gray-800 rounded-2xl p-10 flex flex-col items-center gap-6 w-full max-w-sm">
        
        <div className="flex flex-col items-center gap-2">
          <span className="text-4xl">✅</span>
          <h1 className="text-white text-2xl font-bold">Donezo</h1>
          <p className="text-gray-400 text-sm text-center">
            AI-powered accountability agent.<br />Stop missing deadlines.
          </p>
        </div>

        <button
          onClick={loginWithGoogle}
          className="w-full flex items-center justify-center gap-3 bg-white text-gray-900 font-semibold py-3 px-4 rounded-xl hover:bg-gray-100 transition"
        >
          <img
            src="https://www.google.com/favicon.ico"
            alt="Google"
            className="w-5 h-5"
          />
          Continue with Google
        </button>

        <p className="text-gray-600 text-xs text-center">
          By continuing, you agree to let Donezo judge you for missing deadlines.
        </p>
      </div>
    </div>
  );
}