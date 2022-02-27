from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenPayloadExtended(BaseModel):
    user_id: int
    organization_id: int
    exp: str
    sub: str
