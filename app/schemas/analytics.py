from datetime import datetime

from pydantic import BaseModel


class ClickRecord(BaseModel):
    link_id: str


class ClickResponse(BaseModel):
    id: str
    link_id: str
    ip_address: str
    user_agent: str | None = None
    referrer: str | None = None
    clicked_at: datetime

    model_config = {"from_attributes": True}


class DailyClickCount(BaseModel):
    date: str
    count: int


class AnalyticsResponse(BaseModel):
    total_clicks: int
    daily_clicks: list[DailyClickCount]