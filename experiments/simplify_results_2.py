import json
from pathlib import Path
import argparse

def simplify_json_to_markdown(input_file, output_file):
    # Charger le fichier JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Créer un contenu Markdown
    markdown_content = []

    # Ajouter la partie "CONFIG"
    markdown_content.append("# CONFIG\n")
    config = data.get('CONFIG', {})
    for key, value in config.items():
        markdown_content.append(f"- **{key}**: {value}\n")

    # Ajouter les statistiques globales
    markdown_content.append("\n# Global Statistics\n")
    markdown_content.append(f"- **Total Challenges**: {data.get('total challenges', 0)}\n")
    markdown_content.append(f"- **Success**: {data.get('success', 0)}\n")
    markdown_content.append(f"- **Pending**: {data.get('pending', 0)}\n")
    markdown_content.append(f"- **Compilation Error**: {data.get('compilation error', 0)}\n")
    markdown_content.append(f"- **Judgment Error**: {data.get('judgment error', 0)}\n")

    # Ajouter les défis échoués
    markdown_content.append("\n# Failed Challenges\n")
    failed_challenges = data.get('failed challenges', {})
    markdown_content.append("## Compilation Errors\n")
    for challenge in failed_challenges.get('compilation error', []):
        markdown_content.append(f"- **Challenge**: {challenge.get('challenge', '')}\n")
        markdown_content.append(f"  - **Error**: {challenge.get('error', '')}\n")
        markdown_content.append(f"  - **Ground Truth**: {challenge.get('ground_truth', '')}\n")

    markdown_content.append("## Judgment Errors\n")
    for challenge in failed_challenges.get('judgment error', []):
        markdown_content.append(f"- **Challenge**: {challenge.get('challenge', '')}\n")
        markdown_content.append(f"  - **Error**: {', '.join(challenge.get('error', []))}\n")
        markdown_content.append(f"  - **Ground Truth**: {challenge.get('ground_truth', '')}\n")

    # Ajouter les détails des challenges
    markdown_content.append("\n# Challenge Details\n")
    for detail in data.get('details', []):
        markdown_content.append(f"## {Path(detail.get('challenge_path', '')).name}\n")
        markdown_content.append(f"- **Question**: {detail.get('question', '')}\n")
        markdown_content.append(f"- **Question Type**: {detail.get('question_type', '')}\n")
        markdown_content.append(f"- **Ground Truth**: {detail.get('ground_truth', '')}\n")
        markdown_content.append(f"- **Reference**: {detail.get('ref', '')}\n")
        markdown_content.append(f"- **Compilation Result**: {detail.get('compilation_result', {})}\n")
        markdown_content.append(f"- **Compilation Attempts**: {detail.get('compilation_attempts', 0)}\n")
        markdown_content.append(f"- **Judgment**: {detail.get('judgment', '')}\n")
        markdown_content.append(f"- **Judge Output**: {detail.get('judge_output', '')}\n")
        markdown_content.append(f"- **Judge Attempts**: {detail.get('judge_attempts', '')}\n")
        markdown_content.append(f"- **Final State**: {detail.get('final_state', '')}\n")

    # Sauvegarder le fichier Markdown
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(markdown_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converts a JSON file containing challenge results to a Markdown file.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    args = parser.parse_args()
    
    output_file = args.input_file.replace('.json', '.md')
    simplify_json_to_markdown(args.input_file, output_file)