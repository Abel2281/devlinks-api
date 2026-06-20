import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.click import Click
from app.models.link import Link
from app.models.user import User
from app.schemas.analytics import AnalyticsResponse, DailyClickCount


class AnalyticsService:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user

    async def record_click(
        self,
        link_id: uuid.UUID,
        ip_address: str,
        user_agent: str | None = None,
        referrer: str | None = None,
    ) -> None:
        # Verify link exists and belongs to someone (we don't need to check ownership for public clicks)
        result = await self.db.execute(
            select(Link).where(Link.id == link_id, Link.is_active == True)
        )
        link = result.scalar_one_or_none()
        if not link:
            raise ValueError("Link not found or inactive")

        click = Click(
            id=uuid.uuid4(),
            link_id=link_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
        )
        self.db.add(click)

    async def get_analytics(self) -> AnalyticsResponse:
        # Get all links for the current user
        links_result = await self.db.execute(
            select(Link.id).where(Link.user_id == self.current_user.id)
        )
        link_ids = [row[0] for row in links_result.all()]

        if not link_ids:
            return AnalyticsResponse(total_clicks=0, daily_clicks=[])

        # Get total clicks
        total_result = await self.db.execute(
            select(func.count()).select_from(Click).where(
                Click.link_id.in_(link_ids)
            )
        )
        total_clicks = total_result.scalar() or 0

        # Get daily click counts (last 30 days)
        daily_result = await self.db.execute(
            select(
                cast(Click.clicked_at, Date).label("date"),
                func.count().label("count"),
            )
            .where(
                Click.link_id.in_(link_ids),
                Click.clicked_at >= datetime.now(timezone.utc).date(),
            )
            .group_by(cast(Click.clicked_at, Date))
            .order_by(cast(Click.clicked_at, Date).desc())
        )
        daily_clicks = [
            DailyClickCount(date=str(row.date), count=row.count)
            for row in daily_result.all()
        ]

        return AnalyticsResponse(
            total_clicks=total_clicks,
            daily_clicks=daily_clicks,
        )