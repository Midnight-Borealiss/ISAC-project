import json
import os
import urllib.parse
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les secrets
load_dotenv()

def migrate_json_to_mongo():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    db = client["ismaila_db"]
    collection = db["faq"]

    # 1. Charger le fichier JSON
    with open('infos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Nettoyer la collection actuelle (pour éviter les doublons)
    collection.delete_many({})

    # 3. Insérer les données
    if isinstance(data, list):
        collection.insert_many(data)
        print(f"✅ Succès ! {len(data)} connaissances importées dans MongoDB.")
    else:
        print("❌ Erreur : Le fichier infos.json doit être une liste.")

if __name__ == "__main__":
    migrate_json_to_mongo()