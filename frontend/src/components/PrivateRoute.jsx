/**
 * Component pour protéger les routes authentifiées
 */

import { Navigate } from 'react-router-dom';
import authService from '../services/authService';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = authService.isAuthenticated();

  if (!isAuthenticated) {
    // Rediriger vers la page de login si non authentifié
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default PrivateRoute;
