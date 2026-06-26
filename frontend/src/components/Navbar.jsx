import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  return (
    <nav className="w-full bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      
      <div
        className="flex items-center gap-2 cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        <span className="text-xl">✅</span>
        <span className="text-gray-900 font-bold text-lg">Donezo</span>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1 bg-amber-50 border border-amber-200 rounded-full px-3 py-1">
          <span className="text-sm">🪙</span>
          <span className="text-amber-700 text-sm font-semibold">0</span>
        </div>

        <div className="flex items-center gap-1 bg-orange-50 border border-orange-200 rounded-full px-3 py-1">
          <span className="text-sm">🔥</span>
          <span className="text-orange-700 text-sm font-semibold">0</span>
        </div>

        <img
          src={user?.photoURL}
          alt="avatar"
          className="w-8 h-8 rounded-full cursor-pointer"
          onClick={handleLogout}
          title="Click to logout"
        />
      </div>

    </nav>
  );
}