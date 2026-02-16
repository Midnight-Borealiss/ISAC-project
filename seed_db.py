import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def seed_isac():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["isac_db"]
    
    # Données de test médicales
    protocoles_initiaux = [
        {
            "category": "Céphalées",
            "keywords": "tête, migraine, crâne",
            "response": "Reposez-vous dans une pièce calme et sombre. Hydratez-vous. Si la douleur persiste, consultez un médecin.",
            "red_flags": ["paralysie", "trouble de la parole", "vomissement violent"],
            "status": "valide",
            "timestamp": datetime.now()
        },
        {
            "category": "Fièvre",
            "keywords": "fièvre, chaud, température, brûlant",
            "response": "Découvrez-vous, buvez de l'eau régulièrement et surveillez votre température toutes les 4 heures.",
            "red_flags": ["convulsions", "taches rouges sur la peau", "confusion"],
            "status": "valide",
            "timestamp": datetime.now()
        },
        {
            "category": "Respiratoire",
            "keywords": "toux, rhume, gorge",
            "response": "Lavez-vous le nez au sérum physiologique. Si vous avez du mal à respirer, consultez en urgence.",
            "red_flags": ["lèvres bleues", "sifflement respiratoire", "étouffement"],
            "status": "valide",
            "timestamp": datetime.now()
        }
    ]

    # Insertion
    db.protocoles.delete_many({}) # On nettoie avant (optionnel)
    db.protocoles.insert_many(protocoles_initiaux)
    print("✅ Base ISAC initialisée avec les protocoles de secours !")

if __name__ == "__main__":
    seed_isac()