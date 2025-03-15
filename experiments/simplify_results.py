import json
from pathlib import Path
import argparse

def simplify_json(input_file, output_file):
    # Charger le fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Créer un nouveau dictionnaire pour stocker les données simplifiées
    simplified_data = {}

    # Conserver la partie "CONFIG"
    simplified_data['CONFIG'] = data.get('CONFIG', {})

    # Conserver les parties "total challenges", "success", "pending", "compilation error", "judgment error"
    simplified_data['total challenges'] = data.get('total challenges', 0)
    simplified_data['success'] = data.get('success', 0)
    simplified_data['pending'] = data.get('pending', 0)
    simplified_data['compilation error'] = data.get('compilation error', 0)
    simplified_data['judgment error'] = data.get('judgment error', 0)

    # Simplifier la partie "failed challenges"
    simplified_data['failed challenges'] = {
        'compilation error': [],
        'judgment error': []
    }

    for challenge in data.get('failed challenges', {}).get('judgment error', []):
        simplified_challenge = {
            'challenge': challenge.get('challenge', ''),
            'error': challenge.get('error', []),
            'ground_truth': challenge.get('ground_truth', '')
        }
        simplified_data['failed challenges']['judgment error'].append(simplified_challenge)

    # Simplifier la partie "details"
    simplified_data['details'] = []

    for detail in data.get('details', []):
        simplified_detail = {
            'challenge_path': Path(detail.get('challenge_path', '')).name,
            'question': detail.get('question', ''),
            'question_type': detail.get('question_type', ''),
            'ground_truth': detail.get('ground_truth', ''),
            'ref': detail.get('ref', ''),
            'compilation_result': detail.get('compilation_result', {}),
            'compilation_attempts': detail.get('compilation_attempts', 0),
            'judgment': detail.get('judgment', None),
            'judge_output': detail.get('judge_output', None),
            'judge_attempts': detail.get('judge_attempts', None),
            'final_state': detail.get('final_state', '')
        }
        simplified_data['details'].append(simplified_detail)

    # Sauvegarder le fichier JSON simplifié
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(simplified_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copies and simplifies a JSON file containing challenge results.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    args = parser.parse_args()
    
    simplify_json(args.input_file, 'simplified_' + args.input_file)

