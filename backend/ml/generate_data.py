"""
Script pour générer des données d'entraînement enrichies
Crée des exemples réalistes avec variations de mots-clés
"""

import pandas as pd
import random

# Templates pour générer des variations
facture_keywords = [
    ["FACTURE", "facture", "INVOICE", "Facture N°", "Facture numéro", "FACTURE N°"],
    ["montant", "total", "somme", "prix", "coût", "Total TTC", "Total HT", "Montant dû"],
    ["EUR", "euros", "€", "EURO"],
    ["TVA", "taxe", "T.V.A", "TVA 20%", "TVA applicable"],
    ["Date", "émission", "Date d'émission", "DATE"],
    ["Client", "Destinataire", "À l'attention de", "DESTINATAIRE"],
    ["Référence", "REF", "Numéro", "N°", "Ref"],
    ["Échéance", "Date limite", "Paiement", "À payer avant"],
    ["Prestations", "Services", "Produits", "Articles"],
    ["HT", "hors taxe", "Hors taxes", "Prix HT"],
    ["Quantité", "Qté", "QTE", "Nombre"],
    ["Prix unitaire", "P.U", "Tarif unitaire"],
    ["Société", "Entreprise", "SARL", "SAS", "EURL"],
    ["SIRET", "SIREN", "TVA intracommunautaire"],
    ["Avoir", "Remboursement", "Crédit", "Note de crédit"],
    ["Proforma", "Devis", "Bon de commande"],
    ["Règlement", "Mode de paiement", "Paiement par", "Modalités"],
    ["Virement", "Chèque", "Espèces", "Carte bancaire"],
]

cv_keywords = [
    ["CV", "Curriculum Vitae", "CURRICULUM VITAE", "Curriculum vitae"],
    ["Expérience professionnelle", "Parcours professionnel", "Expériences", "Emplois"],
    ["Formation", "Diplômes", "Études", "Parcours académique"],
    ["Compétences", "Savoir-faire", "Aptitudes", "Qualifications"],
    ["Langues", "Langue maternelle", "Langues parlées"],
    ["Développeur", "Ingénieur", "Chef de projet", "Manager", "Consultant"],
    ["Python", "Java", "JavaScript", "C++", "PHP"],
    ["Master", "Licence", "Doctorat", "Bachelor", "Ingénieur"],
    ["Années d'expérience", "ans d'expérience", "Expérience de"],
    ["Références", "Recommandations", "Contacts"],
    ["Objectif professionnel", "Projet professionnel", "Objectif"],
    ["Portfolio", "Réalisations", "Projets"],
    ["Autonomie", "Rigueur", "Dynamique", "Esprit d'équipe"],
    ["Stage", "Alternance", "CDD", "CDI"],
    ["Poste actuel", "Poste recherché", "Disponibilité"],
]

contrat_keywords = [
    ["Contrat", "CONTRAT", "Convention", "Accord"],
    ["CDI", "CDD", "Contrat à durée indéterminée", "Contrat à durée déterminée"],
    ["Parties", "Entre", "Soussigné", "Signataires"],
    ["Article", "Clause", "Stipulation", "Disposition"],
    ["Durée", "Période", "Terme", "Échéance"],
    ["Rémunération", "Salaire", "Montant", "Honoraires"],
    ["Obligations", "Engagements", "Devoirs", "Responsabilités"],
    ["Résiliation", "Rupture", "Terme", "Fin"],
    ["Préavis", "Délai", "Notice"],
    ["Confidentialité", "Secret", "Non-divulgation", "NDA"],
    ["Propriété intellectuelle", "Droits d'auteur", "Brevets"],
    ["Litige", "Différend", "Arbitrage", "Juridiction"],
    ["Signature", "Fait à", "Date", "Lu et approuvé"],
    ["Employeur", "Salarié", "Entreprise", "Société"],
    ["Mission", "Fonction", "Poste", "Travail"],
]

lettre_keywords = [
    ["Lettre", "Courrier", "Correspondance"],
    ["Madame", "Monsieur", "Madame, Monsieur"],
    ["Objet", "Concerne", "Référence"],
    ["Motivation", "Candidature", "Postule"],
    ["Veuillez agréer", "Cordialement", "Salutations", "Bien à vous"],
    ["Recommandation", "Attestation", "Certificat"],
    ["Démission", "Départ", "Quitter"],
    ["Réclamation", "Contestation", "Plainte"],
    ["Sollicite", "Demande", "Souhaite"],
    ["À l'attention de", "Destinataire", "Pour"],
    ["Mise en demeure", "Sommation", "Avertissement"],
    ["Remerciements", "Gratitude", "Reconnaissance"],
    ["Regrets", "Excuses", "Désolé"],
    ["Invitation", "Convier", "Plaisir"],
    ["Formule de politesse", "Respectueusement"],
]

autre_keywords = [
    ["Notice", "Mode d'emploi", "Instructions", "Manuel"],
    ["Rapport", "Compte rendu", "Bilan", "Analyse"],
    ["Menu", "Carte", "Plats", "Entrées", "Desserts"],
    ["Programme", "Planning", "Calendrier", "Horaires"],
    ["Catalogue", "Brochure", "Prospectus"],
    ["Formulaire", "Questionnaire", "Fiche"],
    ["Certificat médical", "Ordonnance", "Prescription"],
    ["Bulletin", "Relevé", "État"],
    ["Article", "Blog", "Publication", "Post"],
    ["Recette", "Cuisine", "Ingrédients", "Préparation"],
    ["Fiche technique", "Spécifications", "Caractéristiques"],
    ["Attestation", "Justificatif", "Preuve"],
]

def generate_samples(keywords_list, category, num_samples=100):
    """Génère des échantillons variés pour une catégorie"""
    samples = []
    
    for _ in range(num_samples):
        # Sélectionner aléatoirement 5-10 groupes de mots-clés
        num_groups = random.randint(5, 10)
        selected_groups = random.sample(keywords_list, min(num_groups, len(keywords_list)))
        
        # Pour chaque groupe, choisir un mot aléatoire
        text_parts = []
        for group in selected_groups:
            text_parts.append(random.choice(group))
        
        # Mélanger l'ordre
        random.shuffle(text_parts)
        
        # Joiner avec des espaces
        text = " ".join(text_parts)
        
        samples.append({'category': category, 'text': text})
    
    return samples

# Générer des données
print("🚀 Génération des données d'entraînement enrichies...")

all_samples = []

print("📄 Génération Factures...")
all_samples.extend(generate_samples(facture_keywords, "Facture", 150))

print("📄 Génération CV...")
all_samples.extend(generate_samples(cv_keywords, "CV", 150))

print("📄 Génération Contrats...")
all_samples.extend(generate_samples(contrat_keywords, "Contrat", 150))

print("📄 Génération Lettres...")
all_samples.extend(generate_samples(lettre_keywords, "Lettre", 150))

print("📄 Génération Autres...")
all_samples.extend(generate_samples(autre_keywords, "Autre", 150))

# Charger les données existantes
existing_df = pd.read_csv('training_data.csv')
print(f"✅ Données existantes: {len(existing_df)} exemples")

# Combiner avec les nouvelles données
new_df = pd.DataFrame(all_samples)
combined_df = pd.concat([existing_df, new_df], ignore_index=True)

# Mélanger aléatoirement
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Sauvegarder
combined_df.to_csv('training_data.csv', index=False, encoding='utf-8')

print(f"✅ Nouveau fichier créé avec {len(combined_df)} exemples!")
print(f"📊 Répartition:")
print(combined_df['category'].value_counts())
print("\n🎉 Terminé! Vous pouvez maintenant entraîner le modèle avec: python ml/train_model.py")
