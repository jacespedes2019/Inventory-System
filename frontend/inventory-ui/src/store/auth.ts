/**
 * File: auth.ts
 * Description: Zustand store for authentication state and actions.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Manage user authentication state (token, email, role).
 * - Provide actions for login, register, and logout.
 * - Decode JWT payload to extract user role.
 *
 * Notes:
 * - Token is persisted in localStorage for session continuity.
 * - Role is required for RBAC in frontend components.
 */

import { create } from "zustand";
import { AuthRepo, type Role } from "../repositories/auth.repo";

// Helper to decode role from JWT (UI-only, no validation)
function decodeRole(token: string): Role | null {
  try {
    const payload = JSON.parse(atob(token.split(".")[1] || ""));
    return (payload.role as Role) ?? null;
  } catch {
    return null;
  }
}

type AuthState = {
  token: string | null;
  email: string | null;
  role: Role | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, role: Role) => Promise<void>;
  logout: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem("token"),
  email: localStorage.getItem("email"),
  role: (localStorage.getItem("role") as Role | null) ?? null,

  async login(email, password) {
    const token = await AuthRepo.login(email, password);
    const role = decodeRole(token);

    localStorage.setItem("token", token);
    localStorage.setItem("email", email);
    if (role) localStorage.setItem("role", role);

    set({ token, email, role });
  },

  async register(email, password, role) {
    await AuthRepo.register(email, password, role);
    // auto-login after register
    const token = await AuthRepo.login(email, password);
    const decodedRole = decodeRole(token);

    localStorage.setItem("token", token);
    localStorage.setItem("email", email);
    if (decodedRole) localStorage.setItem("role", decodedRole);

    set({ token, email, role: decodedRole });
  },

  logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    localStorage.removeItem("role");
    set({ token: null, email: null, role: null });
  },
}));