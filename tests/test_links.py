import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_link(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/links",
        json={
            "title": "GitHub",
            "url": "https://github.com/testuser",
            "order": 1,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "GitHub"
    assert data["url"] == "https://github.com/testuser"
    assert data["order"] == 1
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_create_link_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/links",
        json={
            "title": "GitHub",
            "url": "https://github.com/testuser",
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_link_javascript_url(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/links",
        json={
            "title": "Bad Link",
            "url": "javascript:alert('xss')",
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_list_links(client: AsyncClient, auth_headers: dict):
    # Create a link first
    await client.post(
        "/api/links",
        json={"title": "GitHub", "url": "https://github.com/testuser"},
        headers=auth_headers,
    )

    # List links
    response = await client.get("/api/links", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "GitHub"


@pytest.mark.asyncio
async def test_update_link(client: AsyncClient, auth_headers: dict):
    # Create a link
    create_resp = await client.post(
        "/api/links",
        json={"title": "GitHub", "url": "https://github.com/testuser"},
        headers=auth_headers,
    )
    link_id = create_resp.json()["id"]

    # Update the link
    response = await client.put(
        f"/api/links/{link_id}",
        json={"title": "GitHub Profile", "order": 2},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "GitHub Profile"
    assert data["order"] == 2


@pytest.mark.asyncio
async def test_update_link_not_found(client: AsyncClient, auth_headers: dict):
    response = await client.put(
        "/api/links/00000000-0000-0000-0000-000000000000",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_link(client: AsyncClient, auth_headers: dict):
    # Create a link
    create_resp = await client.post(
        "/api/links",
        json={"title": "GitHub", "url": "https://github.com/testuser"},
        headers=auth_headers,
    )
    link_id = create_resp.json()["id"]

    # Delete the link
    response = await client.delete(f"/api/links/{link_id}", headers=auth_headers)
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_max_links_limit(client: AsyncClient, auth_headers: dict):
    # Create max links (10)
    for i in range(10):
        response = await client.post(
            "/api/links",
            json={
                "title": f"Link {i}",
                "url": f"https://example.com/{i}",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201

    # Try to create one more
    response = await client.post(
        "/api/links",
        json={"title": "Extra Link", "url": "https://example.com/extra"},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "Maximum" in response.json()["detail"]