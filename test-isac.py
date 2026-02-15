from agent import isac_agent

def run_test():
    print("--- 🏥 DÉMARRAGE DU TEST ISAC ---")
    
    # Simulation d'un profil patient (données venant de la barre latérale)
    profil_test = {"age": 30, "poids": 75, "temperature": 37.5}
    
    # CAS 1 : URGENCE
    print("\n[Test 1: Urgence]")
    query_1 = "J'ai très mal à la poitrine"
    reponse_1, source_1 = isac_agent.get_response(query_1, profil_test, "test_user")
    print(f"Patient: {query_1}")
    print(f"ISAC: {reponse_1}")
    print(f"Source: {source_1}")

    # CAS 2 : CONSEIL SIMPLE
    print("\n[Test 2: Conseil]")
    query_2 = "J'ai le nez qui coule"
    reponse_2, source_2 = isac_agent.get_response(query_2, profil_test, "test_user")
    print(f"Patient: {query_2}")
    print(f"ISAC: {reponse_2}")
    print(f"Source: {source_2}")

if __name__ == "__main__":
    run_test()