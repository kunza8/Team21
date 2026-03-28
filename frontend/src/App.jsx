import { useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import RoleSelect from "./pages/RoleSelect";
import CheckIn from "./pages/CheckIn";
import Dashboard from "./pages/Dashboard";
import StudentProfile from "./pages/StudentProfile";
import Observe from "./pages/Observe";
import CreativeTask from "./pages/CreativeTask";

export default function App() {
  const [role, setRole] = useState(null);
  const [studentId, setStudentId] = useState(null);

  if (!role) {
    return (
      <RoleSelect
        onSelect={(r, sid) => {
          setRole(r);
          if (sid) setStudentId(sid);
        }}
      />
    );
  }

  const homeRoute =
    role === "student"
      ? "/checkin"
      : role === "teacher"
        ? "/observe"
        : "/dashboard";

  return (
    <BrowserRouter>
      <Routes>
        <Route
          element={
            <Layout role={role} onRoleChange={() => { setRole(null); setStudentId(null); }} />
          }
        >
          <Route index element={<Navigate to={homeRoute} replace />} />
          <Route path="/checkin" element={<CheckIn studentId={studentId} />} />
          <Route path="/creative" element={<CreativeTask studentId={studentId} />} />
          <Route path="/observe" element={<Observe />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/students/:id" element={<StudentProfile />} />
          <Route path="*" element={<Navigate to={homeRoute} replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
