/**
 * Page d'upload de documents
 * Permet de téléverser, effectuer l'OCR et classifier automatiquement
 */

import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { uploadDocument, performOCR, classifyDocument } from '../services/api';

const Upload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  
  // Étapes du processus
  const steps = [
    { id: 1, name: 'Upload', icon: '📤', description: 'Téléversement du fichier' },
    { id: 2, name: 'OCR', icon: '👁️', description: 'Extraction du texte' },
    { id: 3, name: 'Classification', icon: '🤖', description: 'Classification IA' },
    { id: 4, name: 'Terminé', icon: '✅', description: 'Traitement terminé' },
  ];
  
  // Gérer le processus complet
  const handleFileSelect = async (file) => {
    setSelectedFile(file);
    setError(null);
    setResult(null);
    setCurrentStep(0);
  };
  
  const processDocument = async () => {
    if (!selectedFile) {
      setError('Veuillez sélectionner un fichier');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setCurrentStep(0);
    
    try {
      // Étape 1: Upload
      setCurrentStep(1);
      const uploadResponse = await uploadDocument(selectedFile);
      console.log('Upload réussi:', uploadResponse);
      
      await delay(500); // Pause pour l'UX
      
      // Étape 2: OCR
      setCurrentStep(2);
      const ocrResponse = await performOCR(uploadResponse.document_id);
      console.log('OCR réussi:', ocrResponse);
      
      await delay(500);
      
      // Étape 3: Classification
      setCurrentStep(3);
      const classifyResponse = await classifyDocument(uploadResponse.document_id);
      console.log('Classification réussie:', classifyResponse);
      
      await delay(500);
      
      // Étape 4: Terminé
      setCurrentStep(4);
      
      // Combiner les résultats
      setResult({
        document_id: uploadResponse.document_id,
        filename: uploadResponse.filename,
        extracted_text: ocrResponse.extracted_text,
        word_count: ocrResponse.word_count,
        language: ocrResponse.language,
        processing_time: ocrResponse.processing_time,
        category: classifyResponse.category,
        confidence: classifyResponse.confidence,
        all_predictions: classifyResponse.all_predictions,
      });
      
    } catch (err) {
      console.error('Erreur:', err);
      setError(err.response?.data?.detail || err.message || 'Une erreur est survenue');
      setCurrentStep(0);
    } finally {
      setIsLoading(false);
    }
  };
  
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  
  const resetProcess = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setCurrentStep(0);
  };
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* En-tête */}
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-3">
              📤 Upload de Document
            </h1>
            <p className="text-gray-600 text-lg font-medium">
              Téléversez un document pour l'analyser avec OCR et IA
            </p>
          </div>
        
          {/* Zone d'upload */}
          <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 mb-6">
            <FileUpload 
              onFileSelect={handleFileSelect}
              isLoading={isLoading}
            />
            
            {/* Bouton de traitement */}
            {selectedFile && !result && (
              <div className="mt-6 text-center">
                <button
                  onClick={processDocument}
                  disabled={isLoading}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-10 py-4 rounded-2xl font-bold text-lg transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-xl hover:shadow-2xl transform hover:scale-105"
                >
                  {isLoading ? '⏳ Traitement en cours...' : '🚀 Analyser le document'}
                </button>
              </div>
            )}
          </div>
        
          {/* Indicateur de progression */}
          {isLoading && (
            <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 mb-6">
              <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-6 text-center">✨ Progression</h3>
              <div className="flex items-center justify-between">
                {steps.map((step, index) => (
                  <React.Fragment key={step.id}>
                    <div className="flex flex-col items-center">
                      <div className={`w-20 h-20 rounded-2xl flex items-center justify-center text-3xl mb-3 transition-all duration-300 shadow-lg ${
                        currentStep >= step.id
                          ? 'bg-gradient-to-br from-green-400 to-emerald-500 text-white scale-110 animate-pulse'
                          : 'bg-gray-200 text-gray-500'
                      }`}>
                        {currentStep > step.id ? '✓' : step.icon}
                      </div>
                      <p className={`text-sm font-bold ${
                        currentStep >= step.id ? 'text-gray-800' : 'text-gray-500'
                      }`}>
                        {step.name}
                      </p>
                      <p className="text-xs text-gray-600 text-center max-w-[100px] font-medium">
                        {step.description}
                      </p>
                    </div>
                    {index < steps.length - 1 && (
                      <div className={`flex-1 h-2 mx-2 rounded-full transition-all duration-300 ${
                        currentStep > step.id ? 'bg-gradient-to-r from-green-400 to-emerald-500' : 'bg-gray-200'
                      }`} />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}
        
          {/* Erreur */}
          {error && (
            <div className="bg-red-50/90 backdrop-blur-xl border-2 border-red-200 rounded-2xl p-6 mb-6 shadow-xl">
              <div className="flex items-start">
                <span className="text-3xl mr-4">❌</span>
                <div>
                  <h3 className="font-bold text-red-800 mb-2 text-xl">Erreur</h3>
                  <p className="text-red-700 font-medium">{error}</p>
                </div>
              </div>
            </div>
          )}
        
          {/* Résultats */}
          {result && (
            <div className="bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  ✅ Analyse Terminée
                </h2>
                <button
                  onClick={resetProcess}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-6 py-3 rounded-xl font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  🆕 Nouveau Document
                </button>
              </div>
            
              {/* Informations générales */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-5 border border-blue-100 shadow-md">
                  <p className="text-sm text-blue-600 font-bold mb-2">📄 Fichier</p>
                  <p className="font-bold text-gray-800 text-lg">{result.filename}</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-5 border border-green-100 shadow-md">
                  <p className="text-sm text-green-600 font-bold mb-2">🆔 ID Document</p>
                  <p className="font-bold text-gray-800 text-lg">#{result.document_id}</p>
                </div>
              </div>
            
              {/* Classification */}
              <div className="bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50 rounded-2xl p-6 mb-6 border border-purple-100 shadow-lg">
                <h3 className="text-2xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  🤖 Classification IA
                </h3>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-5 border border-purple-200 shadow-md">
                    <p className="text-sm text-purple-600 font-bold mb-2">📂 Catégorie</p>
                    <p className="text-3xl font-bold text-purple-700">{result.category}</p>
                  </div>
                  <div className="bg-white/60 backdrop-blur-sm rounded-xl p-5 border border-green-200 shadow-md">
                    <p className="text-sm text-green-600 font-bold mb-2">⭐ Confiance</p>
                    <p className="text-3xl font-bold text-green-600">
                      {(result.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              
                {/* Toutes les prédictions */}
                <div>
                  <p className="text-sm text-gray-700 mb-3 font-bold">
                    📊 Scores de toutes les catégories:
                  </p>
                  <div className="space-y-3">
                    {Object.entries(result.all_predictions).map(([category, score]) => (
                      <div key={category} className="flex items-center">
                        <span className="text-sm font-bold text-gray-700 w-28">
                          {category}
                        </span>
                        <div className="flex-1 bg-gray-200 rounded-full h-8 overflow-hidden shadow-inner">
                          <div
                            className="bg-gradient-to-r from-purple-500 via-pink-500 to-rose-500 h-full flex items-center justify-end pr-3 transition-all duration-500"
                            style={{ width: `${score * 100}%` }}
                          >
                            {score > 0.1 && (
                              <span className="text-xs text-white font-bold">
                                {(score * 100).toFixed(1)}%
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            
              {/* OCR Stats */}
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-5 text-center border border-yellow-100 shadow-md">
                  <p className="text-sm text-orange-600 font-bold mb-2">📝 Mots extraits</p>
                  <p className="text-3xl font-bold text-gray-800">{result.word_count}</p>
                </div>
                <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-5 text-center border border-blue-100 shadow-md">
                  <p className="text-sm text-blue-600 font-bold mb-2">🌐 Langue</p>
                  <p className="text-3xl font-bold text-gray-800">{result.language}</p>
                </div>
                <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-5 text-center border border-green-100 shadow-md">
                  <p className="text-sm text-green-600 font-bold mb-2">⏱️ Temps (s)</p>
                  <p className="text-3xl font-bold text-gray-800">{result.processing_time}</p>
                </div>
              </div>
            
              {/* Texte extrait */}
              <div className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-2xl p-6 border border-gray-200 shadow-md">
                <h3 className="text-xl font-bold mb-4 bg-gradient-to-r from-gray-700 to-blue-700 bg-clip-text text-transparent">
                  👁️ Texte Extrait (OCR)
                </h3>
                <div className="bg-white/80 backdrop-blur-sm rounded-xl p-5 max-h-64 overflow-y-auto border border-gray-300 shadow-inner">
                  <p className="text-sm text-gray-700 whitespace-pre-wrap font-mono leading-relaxed">
                    {result.extracted_text || 'Aucun texte extrait'}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Upload;
