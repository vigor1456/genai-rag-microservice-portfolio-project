from fastapi import Header, HTTPException, status
from app.config import settings

async def require_api_key(x_api_key: str | None = Header(default=None)):
    if settings.api_key:
        if x_api_key != settings.api_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
