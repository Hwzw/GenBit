"""Tests for the construct GenBank export endpoint."""

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.dependencies import get_db
from app.main import app


_CONSTRUCT_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
_PROJECT_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")
_SESSION_ID = "33333333-3333-3333-3333-333333333333"


def _make_element(element_type, label, sequence, position):
    return SimpleNamespace(
        element_type=element_type,
        label=label,
        sequence=sequence,
        position=position,
        metadata_json=None,
    )


def _make_construct(*, with_elements=True, organism_tax_id=None, name="Test Construct"):
    elements = (
        [
            _make_element("promoter", "CMV", "AAAA", 0),
            _make_element("cds", "GFP", "ATGCCCGGG", 1),
            _make_element("terminator", "bGH", "TTTT", 2),
        ]
        if with_elements
        else []
    )
    return SimpleNamespace(
        id=_CONSTRUCT_ID,
        project_id=_PROJECT_ID,
        name=name,
        full_sequence=None,
        organism_tax_id=organism_tax_id,
        elements=elements,
    )


def _override_db_with_project(session_id=_SESSION_ID):
    """Override get_db so project lookups succeed with the given session."""
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(
        return_value=SimpleNamespace(id=_PROJECT_ID, session_id=session_id)
    )
    app.dependency_overrides[get_db] = lambda: mock_session
    return mock_session


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_export_happy_path_returns_genbank_attachment(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project()
    try:
        resp = client.get(
            f"/api/constructs/{_CONSTRUCT_ID}/export",
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert resp.status_code == 200
    cd = resp.headers["content-disposition"]
    assert "attachment" in cd
    assert cd.endswith('.gb"')
    body = resp.text
    assert body.startswith("LOCUS")
    assert "FEATURES" in body
    assert "/label=\"GFP\"" in body
    assert "/label=\"CMV\"" in body


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_export_empty_construct_returns_400(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct(with_elements=False)
    _override_db_with_project()
    try:
        resp = client.get(
            f"/api/constructs/{_CONSTRUCT_ID}/export",
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert resp.status_code == 400
    assert "no elements" in resp.json()["detail"].lower()


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_export_wrong_session_returns_404(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project(session_id="different-session")
    try:
        resp = client.get(
            f"/api/constructs/{_CONSTRUCT_ID}/export",
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert resp.status_code == 404


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_export_unknown_format_returns_422(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project()
    try:
        resp = client.get(
            f"/api/constructs/{_CONSTRUCT_ID}/export?format=snapgene",
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert resp.status_code == 422
