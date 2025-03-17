from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from app.utils.jwt import verify_access_token

security = HTTPBearer()


def get_current_user(required_roles: list[str] = None):
    def _validate_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        payload = verify_access_token(token)

        print(f"🛠 Token décodé : {payload}")  # ✅ Debug: Vérifier le contenu du JWT

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        if required_roles and payload.get("role") not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")

        return payload

    return _validate_user
