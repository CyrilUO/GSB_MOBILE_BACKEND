import json
import os.path
from typing import Set

BLACKLISTED_TOKENS: Set[str] = set()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Remonte à 'GSB_MOBILE_BACKEND'
BLACKLIST_FILE = os.path.join(BASE_DIR, "blacklist.json")  # ✅ Chemin correct

print(f"✔ Fichier blacklist situé à : {BLACKLIST_FILE}")  # ✅ Vérification du chemin


def add_token_to_blacklist(token: str):
    global BLACKLISTED_TOKENS
    BLACKLISTED_TOKENS.add(token)
    try:
        with open(BLACKLIST_FILE, "w") as f:
            json.dump(list(BLACKLISTED_TOKENS), f)
        print(f"✅ Token ajouté à la blacklist : {token}")
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture du fichier blacklist : {e}")


def load_blacklisted_tokens():
    print("Loading blacklisted tokens")
    global BLACKLISTED_TOKENS

    try:
        print(BLACKLIST_FILE)
        with open(BLACKLIST_FILE, "r") as bl:
            BLACKLISTED_TOKENS = set(json.load(bl))
    except (FileNotFoundError, json.JSONDecodeError):
        BLACKLISTED_TOKENS = set()
