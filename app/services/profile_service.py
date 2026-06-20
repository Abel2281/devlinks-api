from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import cache_get, cache_set, cache_delete
from app.core.config import get_settings
from app.models.user import User
from app.models.link import Link

settings = get_settings()


class ProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_profile(self, username: str) -> dict | None:
        # Try cache first
        cache_key = f"profile:{username}"
        cached = await cache_get(cache_key)
        if cached:
            return cached

        # Query database
        result = await self.db.execute(
            select(User).where(User.username == username.lower())
        )
        user = result.scalar_one_or_none()
        if not user:
            return None

        # Get active links
        links_result = await self.db.execute(
            select(Link)
            .where(Link.user_id == user.id, Link.is_active == True)
            .order_by(Link.order)
        )
        links = links_result.scalars().all()

        profile = {
            "username": user.username,
            "display_name": user.display_name,
            "bio": user.bio,
            "profile_image_url": user.profile_image_url,
            "links": [
                {
                    "id": str(link.id),
                    "title": link.title,
                    "url": link.url,
                    "order": link.order,
                }
                for link in links
            ],
        }

        # Cache the profile
        await cache_set(cache_key, profile, settings.PROFILE_CACHE_TTL)

        return profile

    async def invalidate_profile_cache(self, username: str) -> None:
        cache_key = f"profile:{username}"
        await cache_delete(cache_key)