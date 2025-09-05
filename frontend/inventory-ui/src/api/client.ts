/**
 * File: client.ts
 * Description: Axios HTTP client configuration for API requests.
 * Author: Jairo Céspedes
 * Date: 2025-09-05
 *
 * Responsibilities:
 * - Provide a preconfigured Axios instance with base URL and Bearer token support.
 * - Automatically attach Authorization header if a token is present in localStorage.
 *
 * Notes:
 * - Base URL comes from VITE_API_URL defined in .env.
 * - Used by all API calls in stores and components.
 */

import axios from "axios";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Attach Bearer token automatically if present
client.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export default client;