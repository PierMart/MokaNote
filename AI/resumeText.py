import json
import os
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log', 'resumeText.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("resumeText")

# Chemin vers le fichier config.json (à adapter si besoin)
# On suppose que le fichier config.json est à la racine du projet
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

# Fonction pour charger la clé API Mistral depuis config.json
def get_mistral_api_key():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    api_key = config.get('MISTRAL_API_KEY')
    logger.info(f"[DEBUG] Clé API lue depuis config.json : {api_key}")
    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("Merci d'ajouter une clé 'MISTRAL_API_KEY' valide (non vide) dans config.json !")
    return api_key

# Fonction pour résumer un texte avec Mistral-large
def summarize_text_with_mistral(text: str) -> str:
    api_key = get_mistral_api_key()
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    print(f"[DEBUG] Header Authorization envoyé : {headers['Authorization']}")
    if not api_key.startswith("sk-") and len(api_key) < 10:
        print("[ERREUR] La clé API semble incorrecte (format inattendu). Vérifie la valeur dans config.json.")
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {
    "role": "system",
    "content": (
        "Tu es un assistant expert en résumé. "
        "Résume la transcription suivante en français, en un seul paragraphe concis (3 à 5 phrases maximum), "
        "fidèle au contenu, clair, précis et sans ajouter d'informations non présentes dans le texte d'origine."
    )
},
            {"role": "user", "content": f"Résume ce texte en français : {text}"}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    # Récupère le résumé dans la réponse
    return result['choices'][0]['message']['content'].strip()

""" # Exemple d'utilisation (à supprimer ou commenter en prod)
if __name__ == "__main__":
    texte = "Mistral AI est une entreprise spécialisée dans l'intelligence artificielle. Elle développe des modèles de langage performants."
    print(summarize_text_with_mistral(texte))
 """