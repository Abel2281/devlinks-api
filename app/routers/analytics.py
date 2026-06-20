import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.routers.deps import get_current_user
from app.schemas.analytics import ClickRecord, AnalyticsResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.post("/click", status_code=status.HTTP_204_NO_CONTENT)
async def record_click(
    click_data: ClickRecord,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    ip_address = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent")
    referrer = request.headers.get("referer")

    # Use background task to record click asynchronously
    background_tasks.add_task(
        _record_click_task,
        link_id=uuid.UUID(click_data.link_id),
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer,
        db=db,
    )


@router.get("", response_model=AnalyticsResponse)
async def get_analytics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = AnalyticsService(db, current_user)
    return await service.get_analytics()


async def _record_click_task(
    link_id: uuid.UUID,
    ip_address: str,
    user_agent: str | None,
    referrer: str | None,
    db: AsyncSession,
) -> None:
    """Background task to record a click."""
    # We need a new session for the background task
    from app.database import async_session_factory

    async with async_session_factory() as session:
        service = AnalyticsService(session, None)  # type: ignore
        try:
            await service.record_click(
                link_id=link_id,
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
            )
            await session.commit()
        except ValueError:
            # Link not found or inactive - silently ignore
            pass
        except Exception:
            await session.rollback()