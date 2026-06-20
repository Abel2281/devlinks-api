from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.profile_service import ProfileService

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/{username}")
async def get_profile(username: str, db: AsyncSession = Depends(get_db)):
    service = ProfileService(db)
    profile = await service.get_profile(username)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    return profile