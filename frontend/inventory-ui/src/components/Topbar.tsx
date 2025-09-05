import { useAuth } from "../store/auth";


export default function Topbar({ email }: { email: string }) {
  const logout = useAuth((s) => s.logout);
  const role = useAuth((s) => s.role);

  return (
    <header className="bg-white border-b">
      <div className="max-w-6xl mx-auto p-4 flex items-center justify-between">
        <div className="font-semibold">Inventory Dashboard</div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-600">{email} ({role})</span>
          <button className="rounded-lg border px-3 py-1.5" onClick={logout}>Logout</button>
        </div>
      </div>
    </header>
  );
}