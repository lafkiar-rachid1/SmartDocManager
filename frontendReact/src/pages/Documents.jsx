/**
 * Page de liste des documents
 * Affiche tous les documents avec possibilité de filtrer et supprimer
 */

import React, { useState, useEffect } from 'react';
import DocumentCard from '../components/DocumentCard';
import AuthImage from '../components/AuthImage';
import { getDocuments, deleteDocument } from '../services/api';

const Documents = () => {
  const [documents, setDocuments] = useState([]);
  const [filteredDocuments, setFilteredDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterCategory, setFilterCategory] = useState('all');
  const [filterType, setFilterType] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDocument, setSelectedDocument] = useState(null);
  
  // Charger les documents au montage du composant
  useEffect(() => {
    loadDocuments();
  }, []);
  
  // Appliquer les filtres quand ils changent
  useEffect(() => {
    applyFilters();
  }, [documents, filterCategory, filterType, searchTerm]);
  
  const loadDocuments = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (err) {
      setError('Erreur lors du chargement des documents');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  const applyFilters = () => {
    let filtered = [...documents];
    
    // Filtrer par catégorie
    if (filterCategory !== 'all') {
      filtered = filtered.filter(doc => doc.category === filterCategory);
    }
    
    // Filtrer par type
    if (filterType !== 'all') {
      filtered = filtered.filter(doc => doc.file_type === filterType);
    }
    
    // Recherche par nom de fichier
    if (searchTerm) {
      filtered = filtered.filter(doc =>
        doc.filename.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredDocuments(filtered);
  };
  
  const handleDelete = async (documentId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce document ?')) {
      return;
    }
    
    try {
      await deleteDocument(documentId);
      // Recharger les documents
      loadDocuments();
    } catch (err) {
      alert('Erreur lors de la suppression');
      console.error(err);
    }
  };
  
  const handleViewDetails = (document) => {
    setSelectedDocument(document);
  };
  
  const closeModal = () => {
    setSelectedDocument(null);
  };
  
  // Obtenir les catégories uniques
  const categories = ['all', ...new Set(documents.map(doc => doc.category).filter(Boolean))];
  const fileTypes = ['all', ...new Set(documents.map(doc => doc.file_type))];
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* En-tête */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
              📁 Mes Documents
            </h1>
            <p className="text-gray-600 text-lg">
              {filteredDocuments.length} document(s) trouvé(s)
            </p>
          </div>
          <button
            onClick={loadDocuments}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-6 py-3 rounded-xl font-medium transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            🔄 Actualiser
          </button>
        </div>
      
        {/* Filtres */}
        <div className="bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20 p-6 mb-8">
          <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6">🔍 Filtres</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Recherche */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                🔎 Rechercher
              </label>
              <input
                type="text"
                placeholder="Nom du fichier..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 shadow-sm hover:shadow-md"
              />
            </div>
            
            {/* Catégorie */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📂 Catégorie
              </label>
              <select
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 shadow-sm hover:shadow-md"
              >
                {categories.map(cat => (
                  <option key={cat} value={cat}>
                    {cat === 'all' ? 'Toutes' : cat}
                  </option>
                ))}
              </select>
            </div>
            
            {/* Type */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                📄 Type de fichier
              </label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl bg-white/50 backdrop-blur-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 shadow-sm hover:shadow-md"
              >
                {fileTypes.map(type => (
                  <option key={type} value={type}>
                    {type === 'all' ? 'Tous' : type}
                  </option>
                ))}
              </select>
            </div>
        </div>
      </div>
      
        {/* Chargement */}
        {isLoading && (
          <div className="text-center py-12 bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600"></div>
            <p className="mt-6 text-gray-700 text-lg font-medium">Chargement des documents...</p>
          </div>
        )}
      
        {/* Erreur */}
        {error && (
          <div className="bg-red-50/90 backdrop-blur-xl border-2 border-red-200 rounded-2xl p-6 mb-6 shadow-xl">
            <p className="text-red-700 font-medium text-lg">⚠️ {error}</p>
          </div>
        )}
      
      {/* Liste des documents */}
      {!isLoading && !error && (
        <>
            {filteredDocuments.length === 0 ? (
              <div className="text-center py-16 bg-white/70 backdrop-blur-xl rounded-2xl shadow-xl border border-white/20">
                <div className="text-8xl mb-6">📭</div>
                <h3 className="text-2xl font-bold bg-gradient-to-r from-gray-700 to-gray-900 bg-clip-text text-transparent mb-3">
                  Aucun document trouvé
                </h3>
                <p className="text-gray-600 text-lg">
                  Essayez de modifier vos filtres ou uploadez un nouveau document
                </p>
              </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredDocuments.map(document => (
                <DocumentCard
                  key={document.id}
                  document={document}
                  onDelete={handleDelete}
                  onViewDetails={handleViewDetails}
                />
              ))}
            </div>
          )}
        </>
      )}
      
      {/* Modal de détails */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto border border-gray-200">
            {/* En-tête du modal */}
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-indigo-600 border-b border-blue-700 p-6 flex items-center justify-between rounded-t-3xl">
              <h2 className="text-2xl font-bold text-white">
                📄 Détails du Document
              </h2>
              <button
                onClick={closeModal}
                className="text-white hover:bg-white/20 rounded-full w-8 h-8 flex items-center justify-center transition-all duration-300"
              >
                ✕
              </button>
            </div>
            
            {/* Contenu du modal */}
            <div className="p-6">
              {/* Afficher l'image si c'est un fichier IMAGE */}
              {selectedDocument.file_type === 'IMAGE' && (
                <div className="mb-6">
                  <p className="text-sm font-bold text-gray-700 mb-3 flex items-center">
                    <span className="mr-2">🖼️</span> Aperçu de l'image:
                  </p>
                  <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl p-4 border border-gray-200 shadow-inner">
                    <AuthImage 
                      src={`http://localhost:8000/api/documents/${selectedDocument.id}/image`}
                      alt={selectedDocument.filename}
                      className="w-full h-auto rounded-lg shadow-lg"
                    />
                  </div>
                </div>
              )}
              
              {/* Informations */}
              <div className="space-y-4 mb-6">
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 border border-blue-100">
                  <p className="text-sm font-semibold text-blue-600 mb-2">📎 Nom du fichier</p>
                  <p className="font-bold text-gray-800 text-lg">{selectedDocument.filename}</p>
                </div>
                
                {selectedDocument.category && (
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 border border-green-100">
                      <p className="text-sm font-semibold text-green-600 mb-1">📁 Catégorie</p>
                      <p className="font-bold text-gray-800 text-lg">{selectedDocument.category}</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-100">
                      <p className="text-sm font-semibold text-purple-600 mb-1">⭐ Confiance</p>
                      <p className="font-bold text-gray-800 text-lg">
                        {(selectedDocument.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                )}
                
                {selectedDocument.metadata && selectedDocument.metadata.length > 0 && (
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-4 border border-yellow-100">
                      <p className="text-sm font-semibold text-orange-600 mb-1">📊 Nombre de mots</p>
                      <p className="font-bold text-gray-800 text-lg">
                        {selectedDocument.metadata[0].word_count}
                      </p>
                    </div>
                    <div className="bg-gradient-to-br from-cyan-50 to-blue-50 rounded-xl p-4 border border-cyan-100">
                      <p className="text-sm font-semibold text-cyan-600 mb-1">🌐 Langue</p>
                      <p className="font-bold text-gray-800 text-lg">
                        {selectedDocument.metadata[0].language}
                      </p>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Texte extrait */}
              {selectedDocument.extracted_text && (
                <div>
                  <p className="text-sm font-bold text-gray-700 mb-3 flex items-center">
                    <span className="mr-2">📝</span> Texte extrait:
                  </p>
                  <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl p-4 max-h-96 overflow-y-auto border border-gray-200 shadow-inner">
                    <p className="text-sm text-gray-700 whitespace-pre-wrap font-mono leading-relaxed">
                      {selectedDocument.extracted_text}
                    </p>
                  </div>
                </div>
              )}
            </div>
            
            {/* Footer du modal */}
            <div className="border-t border-gray-200 bg-gray-50/50 p-6 flex justify-end space-x-3 rounded-b-3xl">
              <button
                onClick={closeModal}
                className="px-8 py-3 border-2 border-gray-300 rounded-xl hover:bg-white transition-all duration-300 font-medium shadow-sm hover:shadow-md"
              >
                Fermer
              </button>
              <button
                onClick={() => {
                  handleDelete(selectedDocument.id);
                  closeModal();
                }}
                className="px-8 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 transition-all duration-300 font-medium shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                🗑️ Supprimer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
    </div>
  );
};

export default Documents;
