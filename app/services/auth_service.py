import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import TokenResponse, RegisterResponse
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, user_data: UserCreate) -> RegisterResponse:
        # Check if email already exists
        existing_email = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        if existing_email.scalar_one_or_none():
            raise ValueError("Email already registered")

        # Check if username already exists
        existing_username = await self.db.execute(
            select(User).where(User.username == user_data.username.lower())
        )
        if existing_username.scalar_one_or_none():
            raise ValueError("Username already taken")

        # Create user
        user = User(
            id=uuid.uuid4(),
            email=user_data.email,
            username=user_data.username.lower(),
            display_name=user_data.display_name,
            bio=user_data.bio,
            profile_image_url=user_data.profile_image_url,
            hashed_password=hash_password(user_data.password),
        )
        self.db.add(user)
        await self.db.flush()

        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        # Store hashed refresh token
        await self._store_refresh_token(user.id, refresh_token)

        return RegisterResponse(
            id=str(user.id),
            email=user.email,
            username=user.username,
            display_name=user.display_name,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        await self._store_refresh_token(user.id, refresh_token)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid refresh token payload")

        # Verify refresh token exists in DB
        hashed_token = hash_password(refresh_token)
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == uuid.UUID(user_id),
                RefreshToken.hashed_token == hashed_token,
                RefreshToken.expires_at > datetime.now(timezone.utc),
            )
        )
        stored_token = result.scalar_one_or_none()
        if not stored_token:
            raise ValueError("Refresh token not found or expired")

        # Delete old refresh token
        await self.db.delete(stored_token)

        # Issue new tokens
        new_access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})

        await self._store_refresh_token(uuid.UUID(user_id), new_refresh_token)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
        )

    async def logout(self, refresh_token: str) -> None:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Invalid refresh token payload")

        # Delete all refresh tokens for user (logout all sessions)
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.user_id == uuid.UUID(user_id))
        )
        tokens = result.scalars().all()
        for token in tokens:
            await self.db.delete(token)

    async def _store_refresh_token(self, user_id: uuid.UUID, token: str) -> None:
        payload = decode_token(token)
        if not payload:
            raise ValueError("Invalid token")

        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        refresh_token = RefreshToken(
            id=uuid.uuid4(),
            user_id=user_id,
            hashed_token=hash_password(token),
            expires_at=expires_at,
        )
        self.db.add(refresh_token)