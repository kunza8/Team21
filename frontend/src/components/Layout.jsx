import { NavLink, Outlet } from "react-router-dom";
import {
  ClipboardCheck,
  Lightbulb,
  Eye,
  LayoutDashboard,
  LogOut,
} from "lucide-react";

const NAV = {
  student: [
    { to: "/checkin", label: "Check In", icon: ClipboardCheck },
    { to: "/creative", label: "Creative Task", icon: Lightbulb },
  ],
  teacher: [
    { to: "/observe", label: "Log Observation", icon: Eye },
  ],
  counselor: [
    { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  ],
};

const ROLE_LABEL = {
  student: "Student",
  teacher: "Teacher",
  counselor: "Counselor",
};

export default function Layout({ role, onRoleChange }) {
  const links = NAV[role] || [];

  return (
    <div className="flex min-h-screen">
      <aside className="w-56 bg-white border-r border-gray-200 flex flex-col">
        <div className="px-4 pt-5 pb-3">
          <h1 className="text-base font-semibold text-gray-900 tracking-tight">
            हाम्रो विद्यार्थी
          </h1>
          <p className="text-[11px] text-gray-400 mt-0.5">{ROLE_LABEL[role]}</p>
        </div>

        <nav className="flex-1 px-2.5 space-y-0.5">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-gray-100 text-gray-900"
                    : "text-gray-500 hover:bg-gray-50 hover:text-gray-700"
                }`
              }
            >
              <Icon size={16} strokeWidth={1.8} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="px-2.5 pb-3">
          <button
            onClick={onRoleChange}
            className="flex items-center gap-2.5 px-3 py-2 w-full rounded-lg text-sm text-gray-400 hover:text-gray-600 hover:bg-gray-50 transition-colors"
          >
            <LogOut size={16} strokeWidth={1.8} />
            Switch role
          </button>
        </div>
      </aside>

      <main className="flex-1 bg-gray-50 overflow-y-auto">
        <div className="max-w-5xl mx-auto px-6 py-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
