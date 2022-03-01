from jose import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import ValidationError

from .token import TokenPayload
from .oauth import SupabaseAuth
from ..security import ALGORITHM
from ..db import get_db
import src.apps.api.v1.users.domain as domain
from src.config import settings


reusable_oauth2 = SupabaseAuth()

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, audience="authenticated", algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Could not validate credentials."
        )

    if not (user := domain.users.get(db, token_data.sub)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )

    return user
