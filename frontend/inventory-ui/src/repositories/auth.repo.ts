// Purpose: Pure data access for authentication.
import client from "../api/client";

export type Role = "admin" | "user";

export const AuthRepo = {
  login: async (email: string, password: string) => {
    const { data } = await client.post<{ access_token: string }>("/auth/login", { email, password });
    return data.access_token;
  },

  register: async (email: string, password: string, role: Role) => {
    await client.post("/auth/register", { email, password, role });
    // Optionally, return nothing (or a status)
  },
};
