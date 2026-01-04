/**
 * Composant principal de l'application
 * Configure le routeur et la structure globale
 */

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import Accueil from './pages/Accueil';
import Login from './pages/Login';
import Register from './pages/Register';
import Upload from './pages/Upload';
import Documents from './pages/Documents';
import Dashboard from './pages/Dashboard';
import authService from './services/authService';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Fonction pour vérifier l'authentification
  const checkAuth = () => {
    try {
      const authenticated = authService.isAuthenticated();
      setIsAuthenticated(authenticated);
    } catch (error) {
      console.error('Erreur lors de la vérification de l\'authentification:', error);
      setIsAuthenticated(false);
    }
  };

  useEffect(() => {
    // Vérifier l'authentification au chargement
    checkAuth();
    setIsLoading(false);

    // Écouter les changements d'authentification
    const handleAuthChange = () => {
      checkAuth();
    };

    window.addEventListener('auth-change', handleAuthChange);
    
    // Nettoyer l'écouteur
    return () => {
      window.removeEventListener('auth-change', handleAuthChange);
    };
  }, []);

  // Debug: afficher l'état d'authentification
  console.log('🔐 État authentification:', isAuthenticated);
  console.log('📍 URL actuelle:', window.location.pathname);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Barre de navigation uniquement si connecté */}
        {isAuthenticated && <Navbar />}
        
        {/* Contenu principal */}
        <main>
          <Routes>
            {/* Route d'accueil publique */}
            <Route 
              path="/" 
              element={isAuthenticated ? <Navigate to="/upload" /> : <Accueil />} 
            />

            {/* Routes publiques */}
            <Route 
              path="/login" 
              element={isAuthenticated ? <Navigate to="/upload" /> : <Login />} 
            />
            <Route 
              path="/register" 
              element={isAuthenticated ? <Navigate to="/upload" /> : <Register />} 
            />

            {/* Routes protégées */}
            <Route 
              path="/upload" 
              element={
                <PrivateRoute>
                  <Upload />
                </PrivateRoute>
              } 
            />
            <Route 
              path="/documents" 
              element={
                <PrivateRoute>
                  <Documents />
                </PrivateRoute>
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
