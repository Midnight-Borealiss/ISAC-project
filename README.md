# 🏥 ISAC - Assistant de Santé Augmenté & Connecté

**ISAC** est un assistant médical intelligent conçu pour orienter les patients, collecter les constantes vitales et faciliter le triage clinique. Initialement basé sur le moteur ISMaiLa, ISAC a été transformé pour répondre aux exigences du secteur de la santé (E-Santé).



---

## 🚀 Fonctionnalités Clés

* **Triage Intelligent (Red Flags)** : Détection automatique des mots-clés d'urgence vitale avec alertes immédiates (SAMU/Urgences).
* **Collecte de Constantes** : Formulaire intégré en barre latérale pour l'âge, le poids et la température.
* **Anamnèse Dynamique** : Aide le patient à structurer son récit de symptômes pour le médecin.
* **Espace Praticien (Admin)** : Tableau de bord permettant aux médecins de consulter les bilans et de valider les protocoles de soins.
* **Architecture Data-Driven** : Base de connaissances gérée via MongoDB pour une mise à jour en temps réel sans modification du code.

## 🛠️ Stack Technique

* **Interface** : [Streamlit](https://streamlit.io/)
* **Intelligence** : Moteur de triage hybride (Mots-clés & LLM ready)
* **Base de Données** : [MongoDB Atlas](https://www.mongodb.com/atlas)
* **Backend** : Python 3.12+

---

## 📂 Structure du Projet

```text
ISAC/
├── streamlit_app.py     # Point d'entrée de l'application
├── agent.py             # Logique de triage et moteur de réponse
├── db_connector.py      # Connexion sécurisée à MongoDB Atlas
├── admin_view.py        # Interface dédiée aux médecins
├── chat_view.py         # Interface de consultation patient
├── seed_db.py           # Script d'initialisation des protocoles médicaux
└── requirements.txt     # Dépendances du projet