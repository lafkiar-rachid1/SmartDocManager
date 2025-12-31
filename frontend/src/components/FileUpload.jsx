/**
 * Composant de téléversement de fichiers
 * Permet de drag & drop ou sélectionner des fichiers
 */

import React, { useState, useRef } from 'react';

const FileUpload = ({ onFileSelect, isLoading }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);
  
  // Gestion du drag & drop
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };
  
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };
  
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };
  
  // Gestion de la sélection de fichier
  const handleFileSelection = (file) => {
    // Vérifier le type de fichier
    const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg', 'image/jpg'];
    
    if (!allowedTypes.includes(file.type)) {
      alert('Type de fichier non supporté. Formats acceptés: PDF, PNG, JPG');
      return;
    }
    
    // Vérifier la taille (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      alert('Fichier trop volumineux. Taille maximale: 10MB');
      return;
    }
    
    setSelectedFile(file);
    onFileSelect(file);
  };
  
  const handleFileInputChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };
  
  const handleClick = () => {
    fileInputRef.current?.click();
  };
  
  const resetFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  return (
    <div className="w-full">
      {/* Zone de drop */}
      <div
        className={`border-3 border-dashed rounded-lg p-8 transition-all duration-200 cursor-pointer ${
          isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
        } ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={!isLoading ? handleClick : undefined}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept=".pdf,.png,.jpg,.jpeg"
          onChange={handleFileInputChange}
          disabled={isLoading}
        />
        
        <div className="text-center">
          {/* Icône */}
          <div className="text-6xl mb-4">
            {isLoading ? '⏳' : selectedFile ? '✅' : '📤'}
          </div>
          
          {/* Texte */}
          {selectedFile ? (
            <div>
              <p className="text-lg font-semibold text-green-600 mb-2">
                Fichier sélectionné
              </p>
              <p className="text-gray-600 mb-1">{selectedFile.name}</p>
              <p className="text-sm text-gray-500">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
              {!isLoading && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    resetFile();
                  }}
                  className="mt-3 text-sm text-red-600 hover:text-red-800 underline"
                >
                  Choisir un autre fichier
                </button>
              )}
            </div>
          ) : (
            <div>
              <p className="text-lg font-semibold text-gray-700 mb-2">
                Glissez-déposez votre document ici
              </p>
              <p className="text-gray-500 mb-4">ou cliquez pour sélectionner</p>
              <p className="text-sm text-gray-400">
                Formats acceptés: PDF, PNG, JPG (max 10MB)
              </p>
            </div>
          )}
        </div>
      </div>
      
      {/* Message de chargement */}
      {isLoading && (
        <div className="mt-4 text-center">
          <div className="inline-flex items-center space-x-2 text-primary-600">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
            <span>Traitement en cours...</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
