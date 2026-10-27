import { Navigate } from "react-router-dom";
import { getCurrentUser, getToken } from "../pages/utils/auth.js";

export default function ProtectedRoute({ children }) {
  const user = getCurrentUser();
  const token = getToken();

  // Require both a stored user object AND a token
  if (!user || !token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}