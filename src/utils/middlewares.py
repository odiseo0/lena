import asyncio
from typing import Callable, Type

from fastapi import Response, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status


class TimeoutMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Type[Response]:
        try:
            response = await asyncio.wait_for(call_next(request), timeout=15)
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT, 
                detail="No timely response could be obtained."
            )

        return response
