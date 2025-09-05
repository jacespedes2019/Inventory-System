import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { useAuth } from "../store/auth";

const signinSchema = z.object({
  email: z.string().email(),
  password: z.string().min(4),
});

const signupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(4),
  role: z.enum(["user", "admin"]),
});

type SignInValues = z.infer<typeof signinSchema>;
type SignUpValues = z.infer<typeof signupSchema>;

export default function LoginPage() {
  const [tab, setTab] = useState<"signin" | "signup">("signin");
  const [err, setErr] = useState<string | null>(null);

  const login = useAuth((s) => s.login);
  const registerUser = useAuth((s) => s.register);
  const nav = useNavigate();

  const si = useForm<SignInValues>({ resolver: zodResolver(signinSchema) });
  const su = useForm<SignUpValues>({
    resolver: zodResolver(signupSchema),
    defaultValues: { role: "user" },
  });

  const onSignIn = async (v: SignInValues) => {
    setErr(null);
    try {
      await login(v.email, v.password);
      nav("/");
    } catch (e: any) {
      setErr(e?.response?.data?.detail || "Invalid credentials");
    }
  };

  const onSignUp = async (v: SignUpValues) => {
    setErr(null);
    try {
      await registerUser(v.email, v.password, v.role);
      nav("/");
    } catch (e: any) {
      const msg =
        e?.response?.data?.detail ||
        (Array.isArray(e?.response?.data) ? e.response.data[0]?.msg : null) ||
        "Registration failed";
      setErr(msg);
    }
  };

  return (
    <div className="min-h-screen grid place-items-center bg-gray-100">
      <div className="w-full max-w-md bg-white rounded-2xl shadow p-6">
        <h1 className="text-2xl font-semibold text-center mb-4">Inventory</h1>

        {/* Tabs */}
        <div className="grid grid-cols-2 rounded-xl overflow-hidden border mb-6">
          <button
            className={`py-2 ${tab === "signin" ? "bg-black text-white" : "bg-white"}`}
            onClick={() => setTab("signin")}
          >
            Sign in
          </button>
          <button
            className={`py-2 ${tab === "signup" ? "bg-black text-white" : "bg-white"}`}
            onClick={() => setTab("signup")}
          >
            Sign up
          </button>
        </div>

        {err && <div className="text-sm text-red-600 mb-3">{err}</div>}

        {tab === "signin" ? (
          <form className="space-y-4" onSubmit={si.handleSubmit(onSignIn)}>
            <div>
              <label className="block text-sm font-medium">Email</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 outline-none focus:ring"
                type="email"
                placeholder="you@example.com"
                {...si.register("email")}
              />
              {si.formState.errors.email && (
                <p className="text-sm text-red-600">{si.formState.errors.email.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium">Password</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 outline-none focus:ring"
                type="password"
                placeholder="••••••••"
                {...si.register("password")}
              />
              {si.formState.errors.password && (
                <p className="text-sm text-red-600">{si.formState.errors.password.message}</p>
              )}
            </div>
            <button
              className="w-full rounded-lg bg-black text-white py-2.5 font-medium disabled:opacity-50"
              disabled={si.formState.isSubmitting}
            >
              {si.formState.isSubmitting ? "Signing in..." : "Sign in"}
            </button>
          </form>
        ) : (
          <form className="space-y-4" onSubmit={su.handleSubmit(onSignUp)}>
            <div>
              <label className="block text-sm font-medium">Email</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 outline-none focus:ring"
                type="email"
                placeholder="you@example.com"
                {...su.register("email")}
              />
              {su.formState.errors.email && (
                <p className="text-sm text-red-600">{su.formState.errors.email.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium">Password</label>
              <input
                className="mt-1 w-full rounded-lg border px-3 py-2 outline-none focus:ring"
                type="password"
                placeholder="Choose a password"
                {...su.register("password")}
              />
              {su.formState.errors.password && (
                <p className="text-sm text-red-600">{su.formState.errors.password.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium">Role</label>
              <select
                className="mt-1 w-full rounded-lg border px-3 py-2 outline-none focus:ring"
                {...su.register("role")}
              >
                <option value="user">user</option>
                <option value="admin">admin</option>
              </select>
              {su.formState.errors.role && (
                <p className="text-sm text-red-600">{su.formState.errors.role.message}</p>
              )}
            </div>
            <button
              className="w-full rounded-lg bg-black text-white py-2.5 font-medium disabled:opacity-50"
              disabled={su.formState.isSubmitting}
            >
              {su.formState.isSubmitting ? "Creating account..." : "Create account"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}