from urllib.parse import unquote
from typing import Optional

from fastapi import Request, status, HTTPException
from fastapi.security.utils import get_authorization_scheme_param


class SupabaseAuth():
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            authorization = unquote(request.headers.get("authorization"))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
                
        return param
