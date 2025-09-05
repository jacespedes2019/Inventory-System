import { Navigate } from "react-router-dom";
import type { JSX } from "react";
import { useAuth } from "../store/auth";

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = useAuth((s: { token: any; }) => s.token);
  if (!token) return <Navigate to="/login" replace />;
  return children;
}