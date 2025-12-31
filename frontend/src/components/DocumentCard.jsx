/**
 * Composant carte de document
 * Affiche les informations d'un document avec ses actions
 */

import React from 'react';
import AuthImage from './AuthImage';

const DocumentCard = ({ document, onDelete, onViewDetails }) => {
  // Fonction pour obtenir l'URL de l'image du document
  const getImageUrl = (documentId) => {
    return `http://localhost:8000/api/documents/${documentId}/image`;
  };
  
  // Fonction pour obtenir l'icône selon le type de fichier
  const getFileIcon = (fileType) => {
    switch (fileType) {
      case 'PDF':
        return '📄';
      case 'IMAGE':
        return '🖼️';
      default:
        return '📋';
    }
  };
  
  // Fonction pour obtenir la couleur selon la catégorie
  const getCategoryColor = (category) => {
    const colors = {
      'Facture': 'bg-green-100 text-green-800 border-green-200',
      'CV': 'bg-blue-100 text-blue-800 border-blue-200',
      'Contrat': 'bg-purple-100 text-purple-800 border-purple-200',
      'Lettre': 'bg-yellow-100 text-yellow-800 border-yellow-200',
      'Autre': 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-200';
  };
  
  // Fonction pour formater la date
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  // Fonction pour obtenir le score de confiance avec couleur
  const getConfidenceDisplay = (confidence) => {
    if (!confidence) return null;
    
    const percentage = (confidence * 100).toFixed(1);
    let color = 'text-gray-600';
    
    if (confidence >= 0.8) color = 'text-green-600';
    else if (confidence >= 0.6) color = 'text-yellow-600';
    else color = 'text-red-600';
    
    return <span className={`font-semibold ${color}`}>{percentage}%</span>;
  };
  
  return (
    <div className="bg-white/80 backdrop-blur-xl rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 p-6 border border-white/20 hover:scale-105 hover:-translate-y-1">
      {/* En-tête */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-4 flex-1">
          {/* Afficher l'image si c'est un fichier IMAGE, sinon afficher l'icône */}
          {document.file_type === 'IMAGE' ? (
            <div className="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl overflow-hidden border-2 border-blue-200 shadow-md flex-shrink-0">
              <AuthImage 
                src={getImageUrl(document.id)} 
                alt={document.filename}
                className="w-full h-full object-cover"
              />
            </div>
          ) : (
            <div className="text-4xl bg-gradient-to-br from-blue-100 to-indigo-100 p-3 rounded-xl">{getFileIcon(document.file_type)}</div>
          )}
          <div className="flex-1 min-w-0">
            <h3 className="font-bold text-gray-800 truncate text-lg" title={document.filename}>
              {document.filename}
            </h3>
            <p className="text-xs text-gray-500 font-medium">ID: {document.id}</p>
          </div>
        </div>
      </div>
      
      {/* Badges catégorie et type */}
      <div className="flex flex-wrap gap-2 mb-4">
        {document.category && (
          <span className={`px-4 py-2 rounded-xl text-xs font-bold border shadow-sm ${getCategoryColor(document.category)}`}>
            {document.category}
          </span>
        )}
        <span className="px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 border border-gray-300 shadow-sm">
          {document.file_type}
        </span>
      </div>
      
      {/* Informations */}
      <div className="space-y-2 mb-4">
        {/* Confiance */}
        {document.confidence && (
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Confiance:</span>
            {getConfidenceDisplay(document.confidence)}
          </div>
        )}
        
        {/* Métadonnées */}
        {document.metadata && document.metadata.length > 0 && (
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Mots extraits:</span>
            <span className="font-medium text-gray-800">
              {document.metadata[0].word_count || 0}
            </span>
          </div>
        )}
        
        {/* Date */}
        <div className="flex justify-between items-center text-sm">
          <span className="text-gray-600">Date:</span>
          <span className="text-gray-700 text-xs">
            {formatDate(document.created_at)}
          </span>
        </div>
      </div>
      
      {/* Texte extrait (aperçu) */}
      {document.extracted_text && (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 mb-4 border border-blue-100">
          <p className="text-xs text-blue-600 mb-2 font-bold flex items-center">
            <span className="mr-1">📝</span> Aperçu du texte:
          </p>
          <p className="text-sm text-gray-700 line-clamp-3 leading-relaxed">
            {document.extracted_text.substring(0, 150)}
            {document.extracted_text.length > 150 ? '...' : ''}
          </p>
        </div>
      )}
      
      {/* Actions */}
      <div className="flex space-x-3">
        <button
          onClick={() => onViewDetails(document)}
          className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-4 py-3 rounded-xl text-sm font-bold transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
        >
          📋 Détails
        </button>
        <button
          onClick={() => onDelete(document.id)}
          className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-3 rounded-xl text-sm font-bold transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
        >
          🗑️
        </button>
      </div>
    </div>
  );
};

export default DocumentCard;
