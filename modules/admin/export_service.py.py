import json
from db_connector import mongo_db

def sync_mongo_to_json(filepath="faq_data.json"):
    """Exporte les contributions validées en format JSON pour la FAQ actuelle."""
    valid_data = list(mongo_db.contributions.find({"status": "valide"}, {"_id": 0, "question": 1, "response": 1, "category": 1}))
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(valid_data, f, ensure_ascii=False, indent=4)
    return len(valid_data)