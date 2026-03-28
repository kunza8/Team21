import { useState, useEffect } from "react";
import { ClipboardCheck, Eye, LayoutDashboard, ChevronRight } from "lucide-react";
import { getStudents } from "../api";

const ROLES = [
  {
    id: "student",
    label: "Student",
    description: "Daily check-ins and creative tasks with your buddy",
    icon: ClipboardCheck,
  },
  {
    id: "teacher",
    label: "Teacher",
    description: "Log behavioral observations for your students",
    icon: Eye,
  },
  {
    id: "counselor",
    label: "Counselor",
    description: "Monitor wellbeing, risks, and manage interventions",
    icon: LayoutDashboard,
  },
];

export default function RoleSelect({ onSelect }) {
  const [pickingStudent, setPickingStudent] = useState(false);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    if (pickingStudent) {
      getStudents().then(setStudents).catch(console.error);
    }
  }, [pickingStudent]);

  if (pickingStudent) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="w-full max-w-sm">
          <button
            onClick={() => setPickingStudent(false)}
            className="text-sm text-gray-400 hover:text-gray-600 mb-4 transition-colors"
          >
            &larr; Back
          </button>
          <h2 className="text-lg font-semibold text-gray-900 mb-0.5">
            Who are you?
          </h2>
          <p className="text-sm text-gray-400 mb-5">
            Select your name to continue
          </p>
          <div className="space-y-1.5">
            {students.map((s) => (
              <button
                key={s.id}
                onClick={() => onSelect("student", s.id)}
                className="w-full flex items-center justify-between px-4 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 hover:border-gray-300 hover:bg-gray-50 transition-colors"
              >
                <span>
                  {s.name}{" "}
                  <span className="text-gray-400">— {s.class}</span>
                </span>
                <ChevronRight size={14} className="text-gray-300" />
              </button>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-md text-center">
        <h1 className="text-2xl font-semibold text-gray-900 tracking-tight">
          हाम्रो विद्यार्थी
        </h1>
        <p className="text-sm text-gray-400 mt-1 mb-8">
          Keeping student wellbeing first
        </p>

        <div className="space-y-2.5">
          {ROLES.map(({ id, label, description, icon: Icon }) => (
            <button
              key={id}
              onClick={() =>
                id === "student" ? setPickingStudent(true) : onSelect(id)
              }
              className="w-full flex items-center gap-3.5 px-4 py-3.5 bg-white border border-gray-200 rounded-lg text-left hover:border-gray-300 hover:bg-gray-50 transition-colors group"
            >
              <div className="w-9 h-9 rounded-lg bg-gray-50 flex items-center justify-center group-hover:bg-gray-100 transition-colors shrink-0">
                <Icon size={18} strokeWidth={1.8} className="text-gray-500" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">{label}</p>
                <p className="text-xs text-gray-400 mt-0.5">{description}</p>
              </div>
              <ChevronRight
                size={14}
                className="text-gray-300 group-hover:text-gray-400 transition-colors shrink-0"
              />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
