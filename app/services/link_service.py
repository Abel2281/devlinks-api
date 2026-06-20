import uuid

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.link import Link
from app.models.user import User
from app.schemas.link import LinkCreate, LinkUpdate, LinkResponse


class LinkService:
    MAX_LINKS = 10

    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user

    async def list_links(self) -> list[LinkResponse]:
        result = await self.db.execute(
            select(Link)
            .where(Link.user_id == self.current_user.id)
            .order_by(Link.order)
        )
        links = result.scalars().all()
        return [
            LinkResponse(
                id=str(link.id),
                title=link.title,
                url=link.url,
                order=link.order,
                is_active=link.is_active,
                created_at=link.created_at,
                updated_at=link.updated_at,
            )
            for link in links
        ]

    async def create_link(self, link_data: LinkCreate) -> LinkResponse:
        # Check max links limit
        result = await self.db.execute(
            select(func.count()).select_from(Link).where(
                Link.user_id == self.current_user.id
            )
        )
        count = result.scalar() or 0
        if count >= self.MAX_LINKS:
            raise ValueError(f"Maximum of {self.MAX_LINKS} links allowed")

        link = Link(
            id=uuid.uuid4(),
            user_id=self.current_user.id,
            title=link_data.title,
            url=link_data.url,
            order=link_data.order,
            is_active=link_data.is_active,
        )
        self.db.add(link)
        await self.db.flush()

        return LinkResponse(
            id=str(link.id),
            title=link.title,
            url=link.url,
            order=link.order,
            is_active=link.is_active,
            created_at=link.created_at,
            updated_at=link.updated_at,
        )

    async def update_link(
        self, link_id: uuid.UUID, link_data: LinkUpdate
    ) -> LinkResponse:
        result = await self.db.execute(
            select(Link).where(
                Link.id == link_id,
                Link.user_id == self.current_user.id,
            )
        )
        link = result.scalar_one_or_none()
        if not link:
            raise ValueError("Link not found")

        if link_data.title is not None:
            link.title = link_data.title
        if link_data.url is not None:
            link.url = link_data.url
        if link_data.order is not None:
            link.order = link_data.order
        if link_data.is_active is not None:
            link.is_active = link_data.is_active

        await self.db.flush()

        return LinkResponse(
            id=str(link.id),
            title=link.title,
            url=link.url,
            order=link.order,
            is_active=link.is_active,
            created_at=link.created_at,
            updated_at=link.updated_at,
        )

    async def delete_link(self, link_id: uuid.UUID) -> None:
        result = await self.db.execute(
            select(Link).where(
                Link.id == link_id,
                Link.user_id == self.current_user.id,
            )
        )
        link = result.scalar_one_or_none()
        if not link:
            raise ValueError("Link not found")

        await self.db.delete(link)