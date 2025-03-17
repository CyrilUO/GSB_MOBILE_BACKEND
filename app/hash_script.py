from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mot de passe en clair
plain_password = "admin"

# Générer un hash
hashed_password = pwd_context.hash(plain_password)

print(f"Mot de passe haché : {hashed_password}")

hashed = bcrypt.hashpw(b"testpassword", bcrypt.gensalt())
print(hashed.decode())


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("mypassword")
print("Hashed password:", hashed_password)

is_valid = pwd_context.verify("mypassword", hashed_password)
print("Password is valid:", is_valid)
