from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from pydantic import ValidationError

from app.db.database import AsyncSessionLocal
from app.db.models import User
from app.schemas.token import TokenPayload
from app.core.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/auth/login")


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
        session: AsyncSession = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate (invalid token)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = token_data.sub
    if user_id is None:
        raise HTTPException(status_code=401, detail="Wrong token format")

    stmt = select(User).where(User.id == int(user_id))
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User not active")

    return user
