"""
Page Dashboard - Statistiques et visualisations
Affiche des graphiques et métriques sur les documents
"""

import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.auth_service import AuthService
from services.api_service import APIService

# Configuration de la page
st.set_page_config(
    page_title="Dashboard - SmartDocManager",
    page_icon="📊",
    layout="wide"
)

# CSS personnalisé - Mode Sombre
st.markdown("""
<style>
    /* Style général */
    .stApp {
        background-color: #0F172A !important;
    }
    
    .main {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Masquer le padding par défaut */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Cartes de statistiques */
    .stat-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(20px);
        padding: 2rem 1.5rem;
        border-radius: 1.5rem;
        border: 2px solid rgba(255,255,255,0.1);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(139, 92, 246, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .stat-value {
        font-size: 3rem;
        font-weight: 900;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: -0.02em;
        color: #F8FAFC;
    }
    
    .stat-label {
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        opacity: 0.9;
        color: #94A3B8 !important;
    }
    
    /* Cartes de graphiques */
    .chart-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.5rem;
    }
    
    /* Section header */
    .section-header {
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 3px solid rgba(139, 92, 246, 0.2);
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Progress bars */
    .progress-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.85) 100%);
        backdrop-filter: blur(20px);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        width: 100%;
    }
    
    .category-name {
        font-weight: 700;
        font-size: 1.1rem;
        color: #F8FAFC;
        margin: 0;
        padding: 0;
        line-height: 1.5;
    }
    
    .category-stats {
        font-size: 0.9rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 0.5rem;
        padding: 0;
    }
    
    /* Boutons */
    .stButton>button {
        border-radius: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        border-radius: 1rem;
        font-weight: 700;
        color: #F8FAFC !important;
    }
    .streamlit-expanderContent {
        background-color: #1E293B !important;
        color: #E2E8F0 !important;
    }
    
    /* Textes */
    h1, h2, h3 { color: #F8FAFC !important; }
    p, li { color: #CBD5E1 !important; }
</style>
""", unsafe_allow_html=True)

# Vérifier l'authentification
if not AuthService.is_authenticated():
    st.warning("⚠️ Vous devez être connecté pour accéder à cette page")
    st.info("👉 Veuillez vous connecter pour voir votre dashboard")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔐 Se connecter", use_container_width=True, type="primary"):
            st.switch_page("pages/0_Login.py")
    st.stop()

# Initialiser session state
if 'statistics' not in st.session_state:
    st.session_state.statistics = None
if 'category_stats' not in st.session_state:
    st.session_state.category_stats = None

# Fonction pour charger les statistiques
def load_statistics():
    """Charger les statistiques depuis l'API"""
    with st.spinner("📊 Chargement des statistiques..."):
        # Charger les statistiques générales
        result_stats = APIService.get_statistics()
        if result_stats["success"]:
            st.session_state.statistics = result_stats["data"]
        else:
            st.error(f"❌ Erreur statistiques: {result_stats['error']}")
            return False
        
        # Charger les statistiques par catégorie
        result_cat = APIService.get_category_statistics()
        if result_cat["success"]:
            st.session_state.category_stats = result_cat["data"]
        else:
            st.error(f"❌ Erreur catégories: {result_cat['error']}")
            return False
        
        return True

# Charger les statistiques au premier chargement
if st.session_state.statistics is None or st.session_state.category_stats is None:
    load_statistics()

# En-tête
st.markdown("""
<div style='text-align: center; margin-bottom: 2rem;'>
    <h1 style='font-size: 4rem; font-weight: 900; background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>
        📊 Dashboard Analytique
    </h1>
    <p style='font-size: 1.3rem; color: #6b7280; font-weight: 600;'>
        Statistiques et visualisations en temps réel
    </p>
</div>
""", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 3])
with col_btn2:
    if st.button("🔄 Actualiser", use_container_width=True, type="primary"):
        load_statistics()
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Vérifier si les données sont disponibles
if not st.session_state.statistics:
    st.info("📊 Aucune statistique disponible")
    if st.button("📤 Aller à l'upload", type="primary"):
        st.switch_page("pages/2_Upload.py")
    st.stop()

stats = st.session_state.statistics

# Cartes de statistiques principales avec espacement
st.markdown("<div style='margin: 2rem 0;'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    st.markdown(f"""
    <div class='stat-card' style='background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%); color: white;'>
        <div class='stat-icon'>📁</div>
        <div class='stat-value'>{stats.get('total_documents', 0)}</div>
        <div class='stat-label' style='color: rgba(255,255,255,0.95) !important;'>Total Documents</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='stat-card' style='background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%); color: white;'>
        <div class='stat-icon'>📅</div>
        <div class='stat-value'>{stats.get('recent_documents', 0)}</div>
        <div class='stat-label' style='color: rgba(255,255,255,0.95) !important;'>Derniers 7 Jours</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    avg_confidence = stats.get('average_confidence', 0) * 100
    st.markdown(f"""
    <div class='stat-card' style='background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white;'>
        <div class='stat-icon'>🎯</div>
        <div class='stat-value'>{avg_confidence:.1f}%</div>
        <div class='stat-label' style='color: rgba(255,255,255,0.95) !important;'>Confiance Moy.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_words = stats.get('total_words_extracted', 0)
    st.markdown(f"""
    <div class='stat-card' style='background: linear-gradient(135deg, #D97706 0%, #B45309 100%); color: white;'>
        <div class='stat-icon'>📝</div>
        <div class='stat-value'>{total_words:,}</div>
        <div class='stat-label' style='color: rgba(255,255,255,0.95) !important;'>Mots Extraits</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Section graphiques
st.markdown("""
<div class='section-header'>
    <div class='section-title'>📈 Visualisations Analytiques</div>
</div>
""", unsafe_allow_html=True)

# Graphiques
if st.session_state.category_stats and st.session_state.category_stats.get('categories'):
    col_chart1, col_chart2 = st.columns(2, gap="large")
    
    categories_data = st.session_state.category_stats['categories']
    
    # Graphique en camembert - Distribution par catégorie
    with col_chart1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">🥧 Distribution par Catégorie</div>', unsafe_allow_html=True)
        
        if stats.get('documents_by_category'):
            df_pie = pd.DataFrame([
                {'Catégorie': k, 'Nombre': v} 
                for k, v in stats['documents_by_category'].items()
            ])
            
            fig_pie = px.pie(
                df_pie, 
                values='Nombre', 
                names='Catégorie',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig_pie.update_traces(
                textposition='auto',
                textinfo='label+percent',
                textfont=dict(size=14, color='white', family='Arial Black'),
                marker=dict(line=dict(color='white', width=3)),
                pull=[0.05] * len(df_pie),
                hovertemplate='<b>%{label}</b><br>Documents: %{value}<br>Pourcentage: %{percent}<extra></extra>'
            )
            
            fig_pie.update_layout(
                showlegend=True,
                height=450,
                margin=dict(t=20, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(size=13, family='Arial', color='#E2E8F0'),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(color='#E2E8F0')
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📊 Pas de données disponibles")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphique en barres - Documents par catégorie
    with col_chart2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">📊 Documents par Catégorie</div>', unsafe_allow_html=True)
        
        if categories_data:
            df_bar = pd.DataFrame(categories_data)
            
            fig_bar = px.bar(
                df_bar,
                x='category',
                y='count',
                text='count',
                color='count',
                color_continuous_scale='Blues',
                labels={'category': 'Catégorie', 'count': 'Nombre de documents'}
            )
            
            fig_bar.update_traces(
                textposition='outside',
                textfont=dict(size=14, color='#E2E8F0', family='Arial Black'),
                marker=dict(line=dict(color='rgb(8,48,107)', width=2)),
                hovertemplate='<b>%{x}</b><br>Documents: %{y}<extra></extra>'
            )
            
            fig_bar.update_layout(
                xaxis_title="",
                yaxis_title="Nombre de documents",
                height=450,
                margin=dict(t=20, b=80, l=50, r=20),
                showlegend=False,
                hovermode='x unified',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(size=13, family='Arial', color='#E2E8F0'),
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=12, color='#E2E8F0')
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    tickfont=dict(size=12, color='#E2E8F0')
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("📊 Pas de données disponibles")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tableau des catégories
    st.markdown("""
    <div class='section-header'>
        <div class='section-title'>📋 Détails par Catégorie</div>
    </div>
    """, unsafe_allow_html=True)
    
    if categories_data:
        # Créer un DataFrame pour l'affichage
        df_display = pd.DataFrame(categories_data)
        
        # Créer le tableau en HTML statique pour éviter les vibrations
        table_html = '<div style="background: #1E293B; border-radius: 1rem; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.3); margin: 1rem 0; border: 1px solid #334155;">'
        table_html += '<table style="width: 100%; border-collapse: collapse;">'
        table_html += '<thead><tr style="background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%); color: white;">'
        table_html += '<th style="padding: 1rem; text-align: left; font-weight: 600; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">Catégorie</th>'
        table_html += '<th style="padding: 1rem; text-align: left; font-weight: 600; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">Nombre</th>'
        table_html += '<th style="padding: 1rem; text-align: left; font-weight: 600; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">Pourcentage</th>'
        table_html += '<th style="padding: 1rem; text-align: left; font-weight: 600; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.05em;">Confiance Moy.</th>'
        table_html += '</tr></thead><tbody>'
        
        for idx, row in df_display.iterrows():
            # Couleur de confiance
            confidence_val = row['avg_confidence'] * 100
            if confidence_val >= 80:
                confidence_color = "#10B981"
            elif confidence_val >= 60:
                confidence_color = "#F59E0B"
            else:
                confidence_color = "#EF4444"
            
            table_html += f'<tr style="border-bottom: 1px solid #334155;">'
            table_html += f'<td style="padding: 1rem; font-weight: 600; color: #E2E8F0;">{row["category"]}</td>'
            table_html += f'<td style="padding: 1rem; color: #94A3B8;">{row["count"]}</td>'
            table_html += f'<td style="padding: 1rem; color: #94A3B8;">{row["percentage"]}%</td>'
            table_html += f'<td style="padding: 1rem; font-weight: 700; color: {confidence_color};">{confidence_val:.1f}%</td>'
            table_html += '</tr>'
        
        table_html += '</tbody></table></div>'
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Afficher aussi avec des barres de progression
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class='section-header'>
            <div class='section-title'>📈 Distribution Visuelle</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Créer toute la structure HTML en une seule fois pour éviter les re-renders
        progress_html = ""
        for idx, row in df_display.iterrows():
            percentage_width = row['percentage']
            progress_html += f"""
            <div class="progress-container" style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="flex: 0 0 150px;">
                        <div class='category-name'>{row['category']}</div>
                    </div>
                    <div style="flex: 1;">
                        <div style="background: #374151; border-radius: 9999px; height: 32px; overflow: hidden; position: relative; box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);">
                            <div style="background: linear-gradient(90deg, #3B82F6 0%, #2563EB 100%); height: 100%; width: {percentage_width}%; transition: width 0.5s ease; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px;">
                                <span style="color: white; font-weight: bold; font-size: 0.875rem;">{percentage_width}%</span>
                            </div>
                        </div>
                        <div class='category-stats' style="margin-top: 0.5rem;">
                            📄 <strong>{row['count']}</strong> documents • 
                            📊 <strong>{row['percentage']}%</strong> • 
                            🎯 Confiance: <strong>{(row['avg_confidence'] * 100):.1f}%</strong>
                        </div>
                    </div>
                </div>
            </div>
            """
        
        st.markdown(progress_html, unsafe_allow_html=True)
    else:
        st.info("📊 Aucune catégorie disponible")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export CSV
    st.markdown("""
    <div class='section-header'>
        <div class='section-title'>📥 Export des Données</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
    
    with col_export1:
        if st.button("📥 Export CSV", use_container_width=True, type="secondary"):
            if categories_data:
                df_export = pd.DataFrame(categories_data)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="💾 Sauvegarder le fichier",
                    data=csv,
                    file_name="statistiques_documents.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Aucune donnée à exporter")
    
    with col_export2:
        if st.button("📊 Export JSON", use_container_width=True, type="secondary"):
            import json
            if categories_data:
                json_str = json.dumps(categories_data, indent=2)
                st.download_button(
                    label="💾 Sauvegarder le fichier",
                    data=json_str,
                    file_name="statistiques_documents.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Aucune donnée à exporter")

else:
    st.info("📊 Aucune statistique de catégorie disponible")
    st.markdown("Uploadez des documents pour voir des statistiques détaillées")
    
    if st.button("📤 Aller à l'upload", type="primary"):
        st.switch_page("pages/2_Upload.py")

# Section d'aide
with st.expander("ℹ️ À propos du Dashboard"):
    st.markdown("""
    ### 📊 Comprendre vos statistiques
    
    - **Total Documents**: Nombre total de documents uploadés et analysés
    - **7 Derniers Jours**: Documents ajoutés récemment
    - **Confiance Moyenne**: Précision moyenne de la classification IA
    - **Mots Extraits**: Total de mots extraits par OCR
    
    ### 📈 Graphiques
    
    - **Camembert**: Montre la distribution proportionnelle des catégories
    - **Barres**: Compare le nombre de documents par catégorie
    - **Tableau**: Détails précis avec pourcentages et confiance
    
    ### 💡 Conseils
    
    - Une confiance > 80% indique une classification très fiable
    - Une confiance entre 60-80% est acceptable
    - Une confiance < 60% peut nécessiter une vérification manuelle
    """)
