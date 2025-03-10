import secrets

secret_key = secrets.token_hex(32)  # Generates a 64-character hex string (256-bit)
print(secret_key)
