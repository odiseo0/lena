from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    aud: Optional[str] = None
    exp: Optional[int] = None
    sub: Optional[str] = None
    email: Optional[str] = None
