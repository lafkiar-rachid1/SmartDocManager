"""
Script d'entraînement du modèle de Machine Learning
Compare plusieurs algorithmes et choisit le meilleur automatiquement
"""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path


def calculate_roc_data(model, model_name, X_test, y_test, classes):
    """
    Calcule les données ROC pour un modèle
    """
    # Binariser les labels
    y_test_bin = label_binarize(y_test, classes=classes)
    
    # Obtenir les probabilités de prédiction
    if hasattr(model, 'predict_proba'):
        y_score = model.predict_proba(X_test)
    elif hasattr(model, 'decision_function'):
        y_score = model.decision_function(X_test)
        from scipy.special import softmax
        y_score = softmax(y_score, axis=1)
    else:
        return None
    
    # Calculer micro-average ROC
    fpr_micro, tpr_micro, _ = roc_curve(y_test_bin.ravel(), y_score.ravel())
    roc_auc_micro = auc(fpr_micro, tpr_micro)
    
    return {
        'fpr': fpr_micro,
        'tpr': tpr_micro,
        'auc': roc_auc_micro,
        'name': model_name
    }


def plot_all_roc_curves(roc_data_list, output_dir='ml/results'):
    """
    Génère un graphique unique avec toutes les courbes ROC et sauvegarde en PNG
    
    Args:
        roc_data_list: Liste des données ROC pour chaque modèle
        output_dir: Dossier de sortie
    """
    # Créer le dossier de sortie
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Créer la figure Plotly
    fig = go.Figure()
    
    # Couleurs modernes pour chaque modèle
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    # Ajouter les courbes ROC pour chaque modèle
    for i, roc_data in enumerate(roc_data_list):
        if roc_data is None:
            continue
            
        fig.add_trace(go.Scatter(
            x=roc_data['fpr'],
            y=roc_data['tpr'],
            mode='lines',
            name=f"{roc_data['name']} (AUC = {roc_data['auc']:.3f})",
            line=dict(color=colors[i % len(colors)], width=3)
        ))
    
    # Ajouter la ligne de référence (aléatoire)
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Aléatoire (AUC = 0.500)',
        line=dict(color='gray', width=2, dash='dash')
    ))
    
    # Personnaliser le layout
    fig.update_layout(
        title=dict(
            text='<b>Comparaison des Courbes ROC - Tous les Modèles</b><br>' +
                 '<sub>Micro-Average ROC pour chaque algorithme</sub>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis=dict(
            title='<b>Taux de Faux Positifs (FPR)</b>',
            title_font=dict(size=14, color='#34495e'),
            gridcolor='rgba(200, 200, 200, 0.3)',
            range=[0, 1]
        ),
        yaxis=dict(
            title='<b>Taux de Vrais Positifs (TPR)</b>',
            title_font=dict(size=14, color='#34495e'),
            gridcolor='rgba(200, 200, 200, 0.3)',
            range=[0, 1.05]
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            bgcolor='rgba(255, 255, 255, 0.9)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1,
            font=dict(size=12)
        ),
        width=1200,
        height=900
    )
    
    # Sauvegarder en PNG
    output_path = Path(output_dir) / "roc_curves_comparison.png"
    fig.write_image(str(output_path), format='png', scale=2)
    
    print(f"\n📊 Courbe ROC comparative sauvegardée: {output_path}")
    print(f"   Résolution: 2400x1800 pixels (haute qualité)")


def prepare_training_data(csv_path='ml/training_data.csv'):
    """
    Charge les données d'entraînement depuis un fichier CSV
    
    Args:
        csv_path: Chemin vers le fichier CSV contenant les données
        
    Returns:
        Tuple (X, y) avec les textes et les labels
    """
    print(f"📂 Chargement des données depuis {csv_path}...")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Le fichier {csv_path} n'existe pas!")
    
    # Charger le CSV
    df = pd.read_csv(csv_path, encoding='utf-8')
    
    print(f"✅ Données chargées: {len(df)} exemples")
    print(f"📊 Répartition par catégorie:")
    print(df['category'].value_counts())
    
    X = df['text'].tolist()
    y = df['category'].tolist()
    
    return X, y

def train_model():
    """
    Entraîne plusieurs modèles de classification et choisit le meilleur
    """
    print("🚀 Démarrage de l'entraînement et comparaison des modèles ML...")
    print("="*80)
    
    # Préparer les données
    X, y = prepare_training_data()
    
    print(f"\n📊 Nombre total d'exemples: {len(X)}")
    print(f"📊 Catégories: {set(y)}")
    
    # Diviser en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📚 Ensemble d'entraînement: {len(X_train)} exemples")
    print(f"🧪 Ensemble de test: {len(X_test)} exemples")
    
    # Créer le vectorizer TF-IDF
    print("\n🔧 Création du vectorizer TF-IDF...")
    vectorizer = TfidfVectorizer(
        max_features=5000,        # Augmenté pour capturer plus de patterns
        ngram_range=(1, 3),       # Unigrammes, bigrammes et trigrammes
        min_df=2,                 # Fréquence minimale
        max_df=0.7,               # Fréquence maximale
        strip_accents='unicode',  # Retirer les accents
        lowercase=True,           # Convertir en minuscules
        sublinear_tf=True         # Échelle logarithmique pour TF
    )
    
    # Transformer les textes en features TF-IDF
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"✅ Vectorisation terminée: {X_train_tfidf.shape[1]} features créées")
    
    # Définir les modèles à tester
    models = {
        "Naive Bayes (Multinomial)": MultinomialNB(alpha=0.1),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=10, random_state=42),
        "Support Vector Machine (Linear)": LinearSVC(C=1.0, max_iter=2000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=20, random_state=42)
    }
    
    print("\n" + "="*80)
    print("🤖 ENTRAÎNEMENT ET COMPARAISON DES MODÈLES")
    print("="*80)
    
    results = {}
    roc_data_list = []  # Pour stocker les données ROC de tous les modèles
    best_model = None
    best_model_name = None
    best_accuracy = 0
    
    # Entraîner et évaluer chaque modèle
    for model_name, model in models.items():
        print(f"\n{'='*80}")
        print(f"📊 Modèle: {model_name}")
        print(f"{'='*80}")
        
        # Mesurer le temps d'entraînement
        start_time = time.time()
        model.fit(X_train_tfidf, y_train)
        train_time = time.time() - start_time
        
        # Prédictions sur TRAIN et TEST
        y_train_pred = model.predict(X_train_tfidf)
        y_test_pred = model.predict(X_test_tfidf)
        
        # Calculer les précisions
        train_accuracy = accuracy_score(y_train, y_train_pred)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        
        # Détection d'overfitting
        overfitting_gap = train_accuracy - test_accuracy
        is_overfitting = overfitting_gap > 0.10  # Si différence > 10%
        
        # Cross-validation (5-fold)
        cv_scores = cross_val_score(model, X_train_tfidf, y_train, cv=5, scoring='accuracy')
        cv_mean = cv_scores.mean()
        cv_std = cv_scores.std()
        
        # Stocker les résultats
        results[model_name] = {
            'model': model,
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'overfitting_gap': overfitting_gap,
            'is_overfitting': is_overfitting,
            'cv_mean': cv_mean,
            'cv_std': cv_std,
            'train_time': train_time,
            'y_pred': y_test_pred
        }
        
        # Afficher les résultats
        print(f"⏱️  Temps d'entraînement: {train_time:.2f}s")
        print(f"🎯 Précision TRAIN: {train_accuracy * 100:.2f}%")
        print(f"🎯 Précision TEST:  {test_accuracy * 100:.2f}%")
        print(f"📊 Écart Train-Test: {overfitting_gap * 100:.2f}%")
        
        # Avertissement overfitting
        if is_overfitting:
            print(f"⚠️  OVERFITTING DÉTECTÉ! (écart > 10%)")
        else:
            print(f"✅ Pas d'overfitting (écart < 10%)")
        
        print(f"📈 Cross-validation (5-fold): {cv_mean * 100:.2f}% (±{cv_std * 100:.2f}%)")
        
        print(f"\n📊 Rapport de classification (TEST):")
        print(classification_report(y_test, y_test_pred, zero_division=0))
        
        # Calculer les données ROC (sans générer de graphique)
        roc_data = calculate_roc_data(model, model_name, X_test_tfidf, y_test, 
                                      classes=sorted(set(y_test)))
        if roc_data:
            roc_data_list.append(roc_data)
            results[model_name]['roc_auc_micro'] = roc_data['auc']
        
        # Mettre à jour le meilleur modèle (basé sur test_accuracy)
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            best_model = model
            best_model_name = model_name
    
    # Générer le graphique ROC comparatif unique
    print("\n" + "="*80)
    print("📈 GÉNÉRATION DU GRAPHIQUE ROC COMPARATIF")
    print("="*80)
    plot_all_roc_curves(roc_data_list, output_dir='ml/results')
    
    # Afficher le récapitulatif
    print("\n" + "="*80)
    print("📊 RÉCAPITULATIF DES PERFORMANCES")
    print("="*80)
    
    # Trier par précision TEST
    sorted_results = sorted(results.items(), key=lambda x: x[1]['test_accuracy'], reverse=True)
    
    print(f"\n{'Rang':<5} {'Modèle':<40} {'Train':<10} {'Test':<10} {'AUC':<10} {'Écart':<10} {'Status'}")
    print("-" * 105)
    
    for rank, (name, result) in enumerate(sorted_results, 1):
        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
        overfitting_icon = "⚠️" if result['is_overfitting'] else "✅"
        auc_micro = result.get('roc_auc_micro', 0)
        print(f"{medal} {rank:<3} {name:<40} {result['train_accuracy']*100:>6.2f}%  "
              f"{result['test_accuracy']*100:>6.2f}%  {auc_micro:>6.3f}   "
              f"{result['overfitting_gap']*100:>6.2f}%  {overfitting_icon}")
    
    # Analyse globale de l'overfitting
    print("\n" + "="*80)
    print("🔍 ANALYSE DE L'OVERFITTING")
    print("="*80)
    
    overfitting_models = [name for name, res in results.items() if res['is_overfitting']]
    
    if overfitting_models:
        print(f"⚠️  Modèles avec overfitting détecté: {', '.join(overfitting_models)}")
        print("💡 Recommandations:")
        print("   - Augmenter les données d'entraînement")
        print("   - Réduire la complexité du modèle")
        print("   - Utiliser plus de régularisation")
    else:
        print("✅ Aucun overfitting détecté sur aucun modèle!")
        print("👍 Tous les modèles généralisent bien aux nouvelles données")
    
    # Sauvegarder le meilleur modèle
    print("\n" + "="*80)
    print(f"🏆 MEILLEUR MODÈLE: {best_model_name}")
    print(f"🎯 Précision TEST: {best_accuracy * 100:.2f}%")
    print(f"📊 Écart Train-Test: {results[best_model_name]['overfitting_gap'] * 100:.2f}%")
    
    if results[best_model_name]['is_overfitting']:
        print(f"⚠️  Attention: Ce modèle présente de l'overfitting")
    else:
        print(f"✅ Ce modèle généralise bien (pas d'overfitting)")
    
    if 'roc_auc_micro' in results[best_model_name]:
        print(f"📈 AUC Micro-Average: {results[best_model_name]['roc_auc_micro']:.3f}")
    
    print("="*80)
    
    print("\n Sauvegarde du meilleur modèle...")
    os.makedirs("ml", exist_ok=True)
    
    joblib.dump(best_model, "ml/model.pkl")
    joblib.dump(vectorizer, "ml/vectorizer.pkl")
    
    # Sauvegarder aussi les infos du modèle
    model_info = {
        'model_name': best_model_name,
        'accuracy': best_accuracy,
        'cv_mean': results[best_model_name]['cv_mean'],
        'cv_std': results[best_model_name]['cv_std'],
        'train_time': results[best_model_name]['train_time']
    }
    joblib.dump(model_info, "ml/model_info.pkl")
    
    print("✅ Meilleur modèle sauvegardé dans ml/model.pkl")
    print("✅ Vectorizer sauvegardé dans ml/vectorizer.pkl")
    print("✅ Informations du modèle sauvegardées dans ml/model_info.pkl")
    
    # Tester quelques prédictions
    print("\n🧪 Test de quelques prédictions:")
    test_examples = [
        "Facture numéro 789 montant total 500 euros TVA incluse",
        "Expérience professionnelle ingénieur Python compétences machine learning",
        "Contrat de travail CDI salaire mensuel clause de confidentialité",
        "Lettre de motivation candidature poste développeur",
        "Article de blog sur les nouvelles technologies"
    ]
    
    for example in test_examples:
        example_tfidf = vectorizer.transform([example])
        prediction = model.predict(example_tfidf)[0]
        probas = model.predict_proba(example_tfidf)[0]
        confidence = max(probas)
        
        print(f"\n📄 Texte: {example[:60]}...")
        print(f"   → Catégorie: {prediction} (confiance: {confidence * 100:.1f}%)")
    
    print("\n✅ Entraînement terminé avec succès!")
    print("🚀 Le modèle est prêt à être utilisé par l'API")

if __name__ == "__main__":
    train_model()
