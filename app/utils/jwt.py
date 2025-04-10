import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt, ExpiredSignatureError

from app import BLACKLISTED_TOKENS
from app.core.config import settings
from app.utils.token_blacklist import load_blacklisted_tokens


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  #24 heures


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Génère un token JWT contenant les données `data`.
    """
    jwt_to_encode = data.copy()

    user_id = data.get('sub')
    if user_id is None:
        raise ValueError('no id in payload')

    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    jwt_to_encode.update({
        "sub": str(user_id),  # Utiliser user_id plutôt qu'un email (JWT plus petit)
        "role": data.get("role"),  # Optionnel, utile pour l'autorisation
        "iat": now.timestamp(),  # Obligatoire pour la sécurité
        "exp": expire.timestamp(),  # Obligatoire pour la sécurité
    })

    encoded_jwt = jwt.encode(jwt_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Type du jwt encodé {type(encoded_jwt)}")
    print(f"Contenu du jwt encodé {encoded_jwt}")

    decoded_token = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": True})
    print(f"JWT généré : {decoded_token}")

    return encoded_jwt


def verify_access_token(token: str):
    load_blacklisted_tokens()

    print(f"Blacklist actuelle en mémoire : {BLACKLISTED_TOKENS}")
    print(f"Vérification blacklist dans `verify_access_token()`: {BLACKLISTED_TOKENS}")
    print(f"Token reçu pour vérification : {token}")  #

    if token in BLACKLISTED_TOKENS:
        print("Token is blacklisted!")
        return None

    print(f"Token non blacklisté : {token}")  #

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                                   options={"verify_exp": False, "leeway": 30})
        print(f"Token decrypted: {decoded_token}")

        exp_time = decoded_token.get("exp")
        current_utc_time = datetime.utcnow().timestamp()
        print(f"System Time: {current_utc_time} | JWT Exp Time: {exp_time}")

        # Verify if there's a significant time difference
        if abs(exp_time - current_utc_time) > 10:
            print("Possible clock drift detected!")

        current_time = datetime.utcnow().timestamp()
        print(f"Exp: {exp_time} | Now: {current_time}")

        if exp_time < current_time:
            print("Token expired!")
            return None

        return decoded_token
    except ExpiredSignatureError:
        print("Token signature expired!")
        return None
    except JWTError as e:
        print(f"JWT validation error: {e}")
        return None
