/**
 * Page Dashboard avec statistiques et graphiques
 * Affiche des visualisations des données
 */

import React, { useState, useEffect } from 'react';
import { getStatistics, getCategoryStats, exportToCSV } from '../services/api';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [categoryStats, setCategoryStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Couleurs pour les graphiques
  const COLORS = ['#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'];
  
  useEffect(() => {
    loadStatistics();
  }, []);
  
  const loadStatistics = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const [statsData, categoryData] = await Promise.all([
        getStatistics(),
        getCategoryStats()
      ]);
      
      setStats(statsData);
      setCategoryStats(categoryData);
    } catch (err) {
      setError('Erreur lors du chargement des statistiques');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleExportCSV = async () => {
    try {
      await exportToCSV();
    } catch (err) {
      alert('Erreur lors de l\'export CSV');
      console.error(err);
    }
  };
  
  // Préparer les données pour le graphique en camembert
  const preparePieData = () => {
    if (!stats || !stats.documents_by_category) return [];
    
    return Object.entries(stats.documents_by_category).map(([name, value]) => ({
      name,
      value
    }));
  };
  
  // Préparer les données pour le graphique en barres
  const prepareBarData = () => {
    if (!categoryStats || !categoryStats.categories) return [];
    
    return categoryStats.categories.map(cat => ({
      name: cat.category,
      documents: cat.count,
      confiance: (cat.avg_confidence * 100).toFixed(1)
    }));
  };
  
  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-4 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Chargement des statistiques...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      {/* En-tête */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
             Dashboard
          </h1>
          <p className="text-gray-600">
            Statistiques et visualisations de vos documents
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={loadStatistics}
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            🔄 Actualiser
          </button>
          <button
            onClick={handleExportCSV}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            📥 Export CSV
          </button>
        </div>
      </div>
      
      {/* Cartes de statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Total documents */}
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold">Total Documents</h3>
            <span className="text-3xl"></span>
          </div>
          <p className="text-4xl font-bold">{stats?.total_documents || 0}</p>
          <p className="text-blue-100 text-sm mt-2">Documents analysés</p>
        </div>
        
        {/* Documents récents */}
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold">7 Derniers Jours</h3>
            <span className="text-3xl"></span>
          </div>
          <p className="text-4xl font-bold">{stats?.recent_documents || 0}</p>
          <p className="text-purple-100 text-sm mt-2">Nouveaux documents</p>
        </div>
        
        {/* Confiance moyenne */}
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold">Confiance Moy.</h3>
            <span className="text-3xl"></span>
          </div>
          <p className="text-4xl font-bold">
            {stats?.average_confidence ? (stats.average_confidence * 100).toFixed(1) : 0}%
          </p>
          <p className="text-green-100 text-sm mt-2">Précision IA</p>
        </div>
        
        {/* Total mots */}
        <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg shadow-lg p-6 text-white">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-semibold">Mots Extraits</h3>
            <span className="text-3xl"></span>
          </div>
          <p className="text-4xl font-bold">
            {stats?.total_words_extracted ? stats.total_words_extracted.toLocaleString() : 0}
          </p>
          <p className="text-yellow-100 text-sm mt-2">Par OCR</p>
        </div>
      </div>
      
      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Graphique en camembert - Distribution par catégorie */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            Distribution par Catégorie
          </h2>
          {preparePieData().length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={preparePieData()}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {preparePieData().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center py-12 text-gray-500">
              Aucune donnée disponible
            </div>
          )}
        </div>
        
        {/* Graphique en barres - Documents par catégorie */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold text-gray-800 mb-4">
            Documents et Confiance par Catégorie
          </h2>
          {prepareBarData().length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={prepareBarData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="documents" fill="#0ea5e9" name="Nombre de documents" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-center py-12 text-gray-500">
              Aucune donnée disponible
            </div>
          )}
        </div>
      </div>
      
      {/* Tableau des catégories */}
      {categoryStats && categoryStats.categories && categoryStats.categories.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="p-6 border-b">
            <h2 className="text-xl font-bold text-gray-800">
              Détails par Catégorie
            </h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Catégorie
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Nombre
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Pourcentage
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Confiance Moy.
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {categoryStats.categories.map((cat, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-medium text-gray-900">{cat.category}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-gray-700">
                      {cat.count}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-32 bg-gray-200 rounded-full h-4 mr-2">
                          <div
                            className="bg-primary-600 h-4 rounded-full"
                            style={{ width: `${cat.percentage}%` }}
                          ></div>
                        </div>
                        <span className="text-sm text-gray-700">{cat.percentage}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`font-semibold ${
                        cat.avg_confidence >= 0.8 ? 'text-green-600' :
                        cat.avg_confidence >= 0.6 ? 'text-yellow-600' :
                        'text-red-600'
                      }`}>
                        {(cat.avg_confidence * 100).toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
      
      {/* Message si aucune donnée */}
      {(!stats || stats.total_documents === 0) && (
        <div className="bg-white rounded-lg shadow-lg p-12 text-center">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-2xl font-semibold text-gray-700 mb-2">
            Aucune statistique disponible
          </h3>
          <p className="text-gray-500 mb-6">
            Uploadez des documents pour voir apparaître les statistiques
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
