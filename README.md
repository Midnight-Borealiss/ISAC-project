# 🎓 ISMaiLa - Assistant Virtuel Intelligent (Groupe ISM)

ISMaiLa est une plateforme collaborative et intelligente conçue pour assister les étudiants du Groupe ISM. Elle combine un Chatbot IA et un système de gestion de connaissances alimenté par la communauté.

## 🚀 Fonctionnalités clés

- **Chatbot Hybride** : Recherche d'abord des réponses validées dans MongoDB avant de solliciter l'IA.
- **Espace Contribution** : Permet aux étudiants de poser des questions et de proposer des réponses.
- **Panel Administration** : Interface sécurisée pour valider les contributions et surveiller les logs.
- **Architecture RAG-Ready** : Structure modulaire facilitant le passage vers une recherche sémantique avancée.

## 📁 Structure du Projet

```text
├── streamlit_app.py      # Point d'entrée unique
├── db_connector.py       # Gestionnaire de base de données MongoDB
├── agent.py              # Logique de décision (DB vs IA)
├── core/                 # Sécurité et authentification
└── modules/              # Modules métiers (Chat, Contribution, Admin)