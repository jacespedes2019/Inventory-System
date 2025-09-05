import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./routes/ProtectedRoute";
import DashboardPage from "./pages/DashboardPage";


export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}