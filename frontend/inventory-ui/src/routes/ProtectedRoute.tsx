/**
 * File: ProtectedRoute.tsx
 * Description: Wrapper component for protecting routes by authentication.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Redirect to login if no token is present in auth store.
 * - Render children if user is authenticated.
 *
 * Notes:
 * - Used in App.tsx to protect Dashboard route.
 */

import { Navigate } from "react-router-dom";
import type { JSX } from "react";
import { useAuth } from "../store/auth";

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = useAuth((s: { token: any; }) => s.token);
  if (!token) return <Navigate to="/login" replace />;
  return children;
}