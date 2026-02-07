/**
 * Page d'accueil publique pour les visiteurs
 * Permet l'analyse de documents sans authentification ni stockage
 */

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FiUploadCloud, FiAlertCircle, FiFileText, FiCheckCircle, FiX, FiZap, FiCpu, FiDatabase } from 'react-icons/fi';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function Accueil() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showBanner, setShowBanner] = useState(true);

  // Gestion du glisser-déposer
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file) => {
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    
    if (!allowedTypes.includes(file.type)) {
      setError('Type de fichier non supporté. Formats acceptés: PDF, JPG, PNG');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('Le fichier est trop volumineux. Taille maximale: 10 MB');
      return;
    }

    setSelectedFile(file);
    setError('');
    setResult(null);
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const analyzeDocument = async () => {
    if (!selectedFile) return;

    setAnalyzing(true);
    setError('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_URL}/api/analyze-guest`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erreur lors de l\'analyse du document');
    } finally {
      setAnalyzing(false);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setResult(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Bannière d'avertissement */}
      {showBanner && (
        <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FiAlertCircle className="text-2xl flex-shrink-0" />
                <div>
                  <p className="font-semibold">Mode Visiteur - Aucune Sauvegarde</p>
                  <p className="text-sm text-amber-50">
                    Vos documents ne sont pas sauvegardés. Dès que vous quittez cette page, tout est effacé. 
                    <Link to="/register" className="ml-2 underline font-semibold hover:text-white">
                      Créez un compte gratuitement
                    </Link> pour bénéficier du stockage permanent de vos documents !
                  </p>
                </div>
              </div>
              <button 
                onClick={() => setShowBanner(false)}
                className="text-white hover:text-amber-100 transition-colors"
              >
                <FiX className="text-xl" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="bg-white/80 backdrop-blur-xl border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                SmartDocManager
              </h1>
              <p className="text-gray-600 mt-2">Analysez vos documents intelligemment avec l'IA</p>
            </div>
            <div className="flex space-x-4">
              <Link 
                to="/login"
                className="px-6 py-2.5 bg-white border-2 border-indigo-600 text-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 transition-all duration-300"
              >
                Connexion
              </Link>
              <Link 
                to="/register"
                className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300"
              >
                Créer un compte
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Essayez notre analyseur de documents gratuitement
          </h2>
          <p className="text-lg text-gray-600">
            Téléchargez un document et découvrez sa catégorie automatiquement grâce à l'intelligence artificielle
          </p>
        </div>

        {/* Zone de téléchargement */}
        {!result && (
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-gray-200">
            <div
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              className={`border-3 border-dashed rounded-2xl p-12 text-center transition-all duration-300 ${
                dragActive 
                  ? 'border-indigo-500 bg-indigo-50' 
                  : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
              }`}
            >
              <FiUploadCloud className={`mx-auto text-6xl mb-4 ${dragActive ? 'text-indigo-500' : 'text-gray-400'}`} />
              
              {selectedFile ? (
                <div>
                  <div className="flex items-center justify-center space-x-2 mb-4">
                    <FiFileText className="text-indigo-600 text-2xl" />
                    <span className="text-lg font-semibold text-gray-900">{selectedFile.name}</span>
                  </div>
                  <p className="text-sm text-gray-500 mb-4">
                    Taille: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <div className="flex justify-center space-x-4">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        analyzeDocument();
                      }}
                      disabled={analyzing}
                      className="px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed z-10 relative"
                    >
                      {analyzing ? (
                        <span className="flex items-center">
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Analyse en cours...
                        </span>
                      ) : (
                        'Analyser le document'
                      )}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        resetForm();
                      }}
                      className="px-8 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all duration-300 z-10 relative"
                    >
                      Annuler
                    </button>
                  </div>
                </div>
              ) : (
                <div className="relative">
                  <input
                    type="file"
                    onChange={handleFileInputChange}
                    accept=".pdf,.jpg,.jpeg,.png"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    disabled={analyzing}
                  />
                  <p className="text-xl font-semibold text-gray-700 mb-2">
                    Glissez-déposez votre document ici
                  </p>
                  <p className="text-gray-500 mb-4">ou cliquez pour parcourir</p>
                  <p className="text-sm text-gray-400">
                    Formats acceptés: PDF, JPG, PNG • Taille max: 10 MB
                  </p>
                </div>
              )}
            </div>

            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start space-x-3">
                <FiAlertCircle className="text-red-500 text-xl flex-shrink-0 mt-0.5" />
                <p className="text-red-700">{error}</p>
              </div>
            )}
          </div>
        )}

        {/* Résultats de l'analyse */}
        {result && (
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 border border-gray-200">
            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <FiCheckCircle className="text-green-600 text-3xl" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Analyse terminée !</h3>
            </div>

            <div className="space-y-6">
              <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-indigo-100">
                <p className="text-sm text-gray-600 mb-2">Catégorie détectée</p>
                <p className="text-3xl font-bold text-indigo-600">{result.category}</p>
              </div>

              <div className="bg-gray-50 rounded-2xl p-6">
                <p className="text-sm text-gray-600 mb-2">Niveau de confiance</p>
                <div className="flex items-center space-x-4">
                  <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
                    <div 
                      className="bg-gradient-to-r from-blue-500 to-indigo-600 h-full rounded-full transition-all duration-1000"
                      style={{ width: `${result.confidence}%` }}
                    ></div>
                  </div>
                  <span className="text-2xl font-bold text-gray-900">{result.confidence.toFixed(1)}%</span>
                </div>
              </div>

              <div className="bg-amber-50 border border-amber-200 rounded-2xl p-6">
                <div className="flex items-start space-x-3">
                  <FiAlertCircle className="text-amber-600 text-xl flex-shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-amber-900 mb-2">Résultat temporaire</p>
                    <p className="text-amber-800 text-sm">
                      Ce document n'a pas été sauvegardé. Pour conserver vos analyses et accéder à l'historique complet,
                      <Link to="/register" className="ml-1 font-semibold underline hover:text-amber-900">
                        créez un compte gratuit
                      </Link>.
                    </p>
                  </div>
                </div>
              </div>

              <button
                onClick={resetForm}
                className="w-full px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:shadow-lg hover:scale-105 transition-all duration-300"
              >
                Analyser un autre document
              </button>
            </div>
          </div>
        )}

        {/* Section avantages */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="group bg-white/80 backdrop-blur-xl rounded-2xl p-8 text-center border-2 border-gray-200 hover:border-indigo-400 hover:shadow-xl transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
              <FiZap className="text-3xl text-indigo-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Analyse rapide</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Classification automatique en quelques secondes grâce à notre moteur d'IA optimisé</p>
          </div>
          <div className="group bg-white/80 backdrop-blur-xl rounded-2xl p-8 text-center border-2 border-gray-200 hover:border-indigo-400 hover:shadow-xl transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
              <FiCpu className="text-3xl text-purple-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Intelligence artificielle</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Modèle de Machine Learning entraîné sur des milliers de documents professionnels</p>
          </div>
          <div className="group bg-white/80 backdrop-blur-xl rounded-2xl p-8 text-center border-2 border-gray-200 hover:border-indigo-400 hover:shadow-xl transition-all duration-300">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-100 to-teal-100 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
              <FiDatabase className="text-3xl text-green-600" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-3">Stockage sécurisé</h3>
            <p className="text-gray-600 text-sm leading-relaxed">Créez un compte pour sauvegarder vos documents et accéder à l'historique complet</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Accueil;
