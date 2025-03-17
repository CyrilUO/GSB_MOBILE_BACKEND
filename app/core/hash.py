from passlib.context import CryptContext

# Création d'un contexte de hachage avec bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hache un mot de passe en utilisant bcrypt.

    :param password: Le mot de passe en clair
    :return: Le mot de passe haché
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe correspond à son hash.

    :param plain_password: Mot de passe en clair
    :param hashed_password: Mot de passe haché
    :return: True si les mots de passe correspondent, sinon False
    """
    return pwd_context.verify(plain_password, hashed_password)
