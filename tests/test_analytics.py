import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_analytics_empty(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/analytics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] == 0
    assert data["daily_clicks"] == []


@pytest.mark.asyncio
async def test_analytics_with_clicks(
    client: AsyncClient, test_user, auth_headers: dict
):
    # Create a link
    create_resp = await client.post(
        "/api/links",
        json={"title": "GitHub", "url": "https://github.com/testuser"},
        headers=auth_headers,
    )
    link_id = create_resp.json()["id"]

    # Record a click
    click_resp = await client.post(
        "/api/analytics/click",
        json={"link_id": link_id},
    )
    assert click_resp.status_code == 204

    # Get analytics
    response = await client.get("/api/analytics", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_clicks"] >= 1


@pytest.mark.asyncio
async def test_click_invalid_link(client: AsyncClient):
    response = await client.post(
        "/api/analytics/click",
        json={"link_id": "00000000-0000-0000-0000-000000000000"},
    )
    # Should return 204 even for invalid links (fire and forget)
    assert response.status_code == 204