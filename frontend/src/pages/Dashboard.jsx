import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStudents, getWatchlist } from "../api";
import {
  AlertTriangle,
  ChevronRight,
  Search,
  Users,
  TrendingDown,
  ShieldCheck,
} from "lucide-react";

const RISK_STYLE = {
  low: "bg-emerald-50 text-emerald-700",
  moderate: "bg-amber-50 text-amber-700",
  high: "bg-red-50 text-red-700",
  crisis: "bg-red-100 text-red-800",
};

function RiskBadge({ level }) {
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium capitalize ${
        RISK_STYLE[level] || "bg-gray-100 text-gray-500"
      }`}
    >
      {level}
    </span>
  );
}

function StatCard({ label, value, icon: Icon }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-400 font-medium">{label}</span>
        <Icon size={16} strokeWidth={1.8} className="text-gray-300" />
      </div>
      <p className="text-2xl font-semibold text-gray-900">{value}</p>
    </div>
  );
}

export default function Dashboard() {
  const [students, setStudents] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getStudents(), getWatchlist()])
      .then(([s, w]) => {
        setStudents(s);
        setWatchlist(w);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const filtered = students.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase())
  );

  const stats = {
    total: students.length,
    flagged: watchlist.length,
    highRisk: students.filter((s) =>
      ["high", "crisis"].includes(s.risk_level)
    ).length,
    healthy: students.filter((s) => s.risk_level === "low").length,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-sm text-gray-400">Loading...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-xl font-semibold text-gray-900">Dashboard</h1>
        <p className="text-sm text-gray-400 mt-1">
          Overview of student wellbeing
        </p>
      </div>

      <div className="grid grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Students" value={stats.total} icon={Users} />
        <StatCard
          label="Needs Attention"
          value={stats.flagged}
          icon={AlertTriangle}
        />
        <StatCard
          label="High Risk"
          value={stats.highRisk}
          icon={TrendingDown}
        />
        <StatCard label="Healthy" value={stats.healthy} icon={ShieldCheck} />
      </div>

      {watchlist.length > 0 && (
        <div className="mb-8">
          <h2 className="text-sm font-medium text-gray-900 mb-3">
            Watchlist
          </h2>
          <div className="bg-white border border-gray-200 rounded-lg divide-y divide-gray-100">
            {watchlist.map((s) => (
              <Link
                key={s.id}
                to={`/students/${s.id}`}
                className="flex items-center justify-between px-4 py-3 hover:bg-gray-50 transition-colors first:rounded-t-lg last:rounded-b-lg"
              >
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-xs font-medium text-gray-500">
                    {s.name.split(" ").map((n) => n[0]).join("")}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {s.name}
                    </p>
                    <p className="text-xs text-gray-400">
                      Class {s.class}
                      {s.risk?.concerns?.[0] && ` — ${s.risk.concerns[0]}`}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <RiskBadge level={s.risk?.risk_level} />
                  <ChevronRight size={16} className="text-gray-300" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      )}

      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-medium text-gray-900">All Students</h2>
          <div className="relative">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-300"
            />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search..."
              className="pl-8 pr-3 py-1.5 text-sm border border-gray-200 rounded-lg bg-white text-gray-700 placeholder-gray-300 focus:outline-none focus:border-gray-400"
            />
          </div>
        </div>
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left px-4 py-2.5 text-xs font-medium text-gray-400">
                  Name
                </th>
                <th className="text-left px-4 py-2.5 text-xs font-medium text-gray-400">
                  Class
                </th>
                <th className="text-left px-4 py-2.5 text-xs font-medium text-gray-400">
                  Last Mood
                </th>
                <th className="text-left px-4 py-2.5 text-xs font-medium text-gray-400">
                  Risk
                </th>
                <th className="text-left px-4 py-2.5 text-xs font-medium text-gray-400">
                  Last Check-in
                </th>
                <th></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {filtered.map((s) => (
                <tr
                  key={s.id}
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td className="px-4 py-3">
                    <Link
                      to={`/students/${s.id}`}
                      className="font-medium text-gray-900 hover:underline"
                    >
                      {s.name}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-gray-500">{s.class}</td>
                  <td className="px-4 py-3 text-gray-700">
                    {s.last_mood ?? "—"} / 5
                  </td>
                  <td className="px-4 py-3">
                    <RiskBadge level={s.risk_level} />
                  </td>
                  <td className="px-4 py-3 text-gray-400">
                    {s.last_checkin_date || "Never"}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Link to={`/students/${s.id}`}>
                      <ChevronRight size={16} className="text-gray-300" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
