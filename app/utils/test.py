import sys
import os

# Ajouter GSB_MOBILE_BACKEND au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.utils.token_blacklist import BLACKLIST_FILE  # ✅ Maintenant, ça fonctionne


if not os.path.exists(BLACKLIST_FILE):
    print(f"🚨 Fichier blacklist.json non trouvé : {BLACKLIST_FILE}")
else:
    print(f"✅ Fichier blacklist.json trouvé : {BLACKLIST_FILE}")
