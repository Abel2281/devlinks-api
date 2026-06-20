import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile_not_found(client: AsyncClient):
    response = await client.get("/api/profile/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_profile_success(client: AsyncClient, test_user, auth_headers: dict):
    # Create a link first
    await client.post(
        "/api/links",
        json={
            "title": "GitHub",
            "url": "https://github.com/testuser",
            "order": 1,
        },
        headers=auth_headers,
    )

    # Get public profile
    response = await client.get("/api/profile/testuser")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["display_name"] == "Test User"
    assert len(data["links"]) == 1
    assert data["links"][0]["title"] == "GitHub"
    assert data["links"][0]["url"] == "https://github.com/testuser"


@pytest.mark.asyncio
async def test_get_profile_inactive_links_hidden(
    client: AsyncClient, test_user, auth_headers: dict
):
    # Create active link
    await client.post(
        "/api/links",
        json={
            "title": "Active",
            "url": "https://example.com/active",
            "is_active": True,
        },
        headers=auth_headers,
    )

    # Create inactive link
    create_resp = await client.post(
        "/api/links",
        json={
            "title": "Inactive",
            "url": "https://example.com/inactive",
            "is_active": False,
        },
        headers=auth_headers,
    )

    # Get profile
    response = await client.get("/api/profile/testuser")
    data = response.json()
    assert len(data["links"]) == 1
    assert data["links"][0]["title"] == "Active"