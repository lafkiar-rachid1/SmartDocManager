/**
 * Composant de navigation principal
 * Affiche le menu de navigation avec les liens vers les différentes pages
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiUpload, FiFolder, FiBarChart2, FiFileText, FiUser, FiLogOut } from 'react-icons/fi';
import authService from '../services/authService';

const Navbar = () => {
  const location = useLocation();
  const user = authService.getCurrentUser();
  
  // Fonction pour déterminer si un lien est actif
  const isActive = (path) => {
    return location.pathname === path;
  };
  
  const handleLogout = () => {
    authService.logout();
  };
  
  const navLinks = [
    { path: '/', label: 'Upload', icon: FiUpload },
    { path: '/documents', label: 'Documents', icon: FiFolder },
    { path: '/dashboard', label: 'Dashboard', icon: FiBarChart2 },
  ];
  
return (
  <nav className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white shadow-2xl backdrop-blur-xl border-b border-white/10">
    <div className="container mx-auto px-4">
      <div className="flex items-center justify-between h-20">
        
        {/* Logo et titre */}
        <div className="flex items-center space-x-4">
          <div className="bg-white/20 p-3 rounded-2xl backdrop-blur-sm border border-white/30 shadow-lg">
            <FiFileText className="text-4xl text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Smart Document Manager</h1>
            <p className="text-xs text-blue-100 font-medium">
              Gestion Intelligente avec OCR et IA
            </p>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex items-center space-x-6">
          <div className="flex space-x-2">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center space-x-2 px-6 py-3 rounded-xl transition-all duration-300 font-semibold ${
                  isActive(link.path)
                    ? 'bg-white/90 text-blue-700 shadow-xl scale-105 backdrop-blur-xl'
                    : 'text-blue-50 hover:bg-white/20 hover:text-white hover:scale-105 backdrop-blur-sm border border-white/10'
                }`}
              >
                <link.icon className="text-xl" />
                <span>{link.label}</span>
              </Link>
            ))}
          </div>

          {/* Info utilisateur et déconnexion */}
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-bold">
                {user?.username || 'Utilisateur'}
              </p>
              <p className="text-xs text-blue-100 font-medium">
                {user?.email || ''}
              </p>
            </div>

            <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-lg border-2 border-white/30">
              <FiUser className="text-2xl text-white" />
            </div>

            <button
              onClick={handleLogout}
              className="px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 rounded-xl transition-all duration-300 font-bold shadow-lg hover:shadow-xl transform hover:scale-105 flex items-center space-x-2"
            >
              <FiLogOut />
              <span>Déconnexion</span>
            </button>
          </div>
        </div>

      </div>
    </div>
  </nav>
  );
};

export default Navbar;