
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings

# Clé secrète et algorithme JWT
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Durée de validité du token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Optional[dict]:
    """
    Génère un token JWT contenant les données `data`.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire.timestamp()})  # Convertir en timestamp UNIX
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> dict or None:
    """
    Vérifie la validité d'un token JWT et retourne les données décodées.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token.get("exp") >= datetime.now(timezone.utc).timestamp() else None
    except JWTError:
        return None

