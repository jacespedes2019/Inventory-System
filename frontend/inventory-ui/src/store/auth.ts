import { create } from "zustand";
import client from "../api/client";

type Role = "admin" | "user";

type AuthState = {
  token: string | null;
  email: string | null;
  role: Role | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, role: Role) => Promise<void>;
  logout: () => void;
};

// decode role from JWT (UI-only, no signature validation)
function decodeRole(token: string): Role | null {
  try {
    const payload = JSON.parse(atob(token.split(".")[1] || ""));
    return (payload.role as Role) ?? null;
  } catch {
    return null;
  }
}

export const useAuth = create<AuthState>((set) => ({
  token: localStorage.getItem("token"),
  email: localStorage.getItem("email"),
  role: (localStorage.getItem("role") as Role | null) ?? null,

  async login(email, password) {
    const { data } = await client.post("/auth/login", { email, password });
    const token = data.access_token as string;
    const role = decodeRole(token);

    localStorage.setItem("token", token);
    localStorage.setItem("email", email);
    if (role) localStorage.setItem("role", role);

    set({ token, email, role });
  },

  async register(email, password, role) {
    await client.post("/auth/register", { email, password, role });
    // auto-login after register
    const { data } = await client.post("/auth/login", { email, password });
    const token = data.access_token as string;
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