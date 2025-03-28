import json
import os.path
from typing import Set

BLACKLISTED_TOKENS: Set[str] = set()

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLACKLIST_FILE = os.path.join(BASE_DIR, "blacklist.json")

print(f"✔Fichier blacklist situé à : {BLACKLIST_FILE}")


def add_token_to_blacklist(token: str):
    global BLACKLISTED_TOKENS
    print(f"Values de ma blacklist dans add Token {BLACKLISTED_TOKENS}")
    BLACKLISTED_TOKENS.add(token)

    try:
        print(f"Tentative d'écriture dans {BLACKLIST_FILE}")
        with open(BLACKLIST_FILE, "w") as f:
            json.dump(list(BLACKLISTED_TOKENS), f)
            f.flush()
            os.fsync(f.fileno())

        print(f"Fichier `blacklist.json` mis à jour avec {token}")

        # Vérifier si le fichier a bien été modifié
        with open(BLACKLIST_FILE, "r") as f:
            print(f"Contenu du fichier après écriture : {f.read()}")

        load_blacklisted_tokens()

    except Exception as e:
        print(f"Erreur lors de l'écriture du fichier blacklist : {e}")


def load_blacklisted_tokens():
    global BLACKLISTED_TOKENS

    print("Chargement des tokens blacklistés...")

    try:
        with open(BLACKLIST_FILE, "r") as bl:
            BLACKLISTED_TOKENS = set(json.load(bl))
        print(f"okens chargés en mémoire : {BLACKLISTED_TOKENS}")
    except FileNotFoundError:
        print("Fichier blacklist.json non trouvé, création d’un nouveau.")
        BLACKLISTED_TOKENS = set()
    except json.JSONDecodeError:
        print("Erreur JSON, blacklist.json corrompu ! Réinitialisation.")
        BLACKLISTED_TOKENS = set()


# Charger la blacklist dès le démarrage
load_blacklisted_tokens()
print(f"BLACKLISTED_TOKENS chargé au démarrage : {BLACKLISTED_TOKENS}")

