from pydantic import BaseModel, Field


class FormData(BaseModel):
    email: str
    password: str
    model_config = {"extra": "forbid"}


class TokenProvider(BaseModel):
    """
    Schéma de réponse pour un token JWT après authentification. Ps : ... means the field is required
    """
    access_token: str = Field(..., description='Contains the entire iat / jti / sub / role encoded in the JWT')
    token_type: str = Field(..., description='the type of bearer')


class LogoutMessage(BaseModel):
    message: str
