import json
import os
from dsl_gen.core import build_rag_flow, CFG, RAGState_to_dict
import os

challenges_path = CFG.PATH_CFG.CHALLENGES_PATH

list_paths = []
for root, dirs, files in os.walk(challenges_path):
    for file in files:
        list_paths.append(os.path.join(root, file))

for file_name in list_paths:
    if not file_name.endswith(".json"):
        continue

    # Étape 1 : Lire le fichier en mode lecture
    with open(file_name, 'r', encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            print(f"Erreur de parsing JSON dans {file_name}")
            continue  # Passer au fichier suivant si le JSON est invalide

    # Étape 2 : Modifier le contenu si nécessaire
    if "answer" in data:
        answer = data["answer"]
        if not answer.startswith("```envision") or not answer.endswith("```"):
            data["answer"] = f"```envision{answer}```"

        # Étape 3 : Écrire le fichier en mode écriture
        with open(file_name, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4)
