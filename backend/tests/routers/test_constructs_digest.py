"""Tests for the construct restriction digest endpoint."""

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.dependencies import get_db
from app.main import app


_CONSTRUCT_ID = uuid.UUID("44444444-4444-4444-4444-444444444444")
_PROJECT_ID = uuid.UUID("55555555-5555-5555-5555-555555555555")
_SESSION_ID = "66666666-6666-6666-6666-666666666666"


def _make_element(element_type, label, sequence, position):
    return SimpleNamespace(
        element_type=element_type,
        label=label,
        sequence=sequence,
        position=position,
        metadata_json=None,
    )


def _make_construct(*, with_elements=True, name="DigestTest"):
    elements = (
        [
            # Layout includes an EcoRI site (GAATTC) inside the CDS.
            _make_element("promoter", "CMV", "AAAAA", 0),
            _make_element("cds", "GOI", "ATGGAATTCAAA", 1),
            _make_element("terminator", "T", "TTTTT", 2),
        ]
        if with_elements
        else []
    )
    return SimpleNamespace(
        id=_CONSTRUCT_ID,
        project_id=_PROJECT_ID,
        name=name,
        full_sequence=None,
        organism_tax_id=None,
        elements=elements,
    )


def _override_db_with_project(session_id=_SESSION_ID):
    mock_session = AsyncMock()
    mock_session.get = AsyncMock(
        return_value=SimpleNamespace(id=_PROJECT_ID, session_id=session_id)
    )
    app.dependency_overrides[get_db] = lambda: mock_session
    return mock_session


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_digest_happy_path(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project()
    try:
        resp = client.post(
            f"/api/constructs/{_CONSTRUCT_ID}/digest",
            json={"enzymes": ["EcoRI"]},
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert resp.status_code == 200
    data = resp.json()
    assert data["enzymes"][0]["name"] == "EcoRI"
    assert data["enzymes"][0]["cut_count"] >= 1
    # The EcoRI site sits inside the GOI CDS, so that annotation should be flagged
    assert "GOI" in data["enzymes"][0]["feature_hits"]
    # Fragments should cover the full sequence
    total = sum(f["length"] for f in data["fragments"])
    assert total == data["sequence_length"]


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_digest_unknown_enzyme_returns_400(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project()
    try:
        resp = client.post(
            f"/api/constructs/{_CONSTRUCT_ID}/digest",
            json={"enzymes": ["Bogus"]},
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)
    assert resp.status_code == 400
    assert "Bogus" in resp.json()["detail"]


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_digest_empty_construct_returns_400(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct(with_elements=False)
    _override_db_with_project()
    try:
        resp = client.post(
            f"/api/constructs/{_CONSTRUCT_ID}/digest",
            json={"enzymes": ["EcoRI"]},
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)
    assert resp.status_code == 400


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_digest_wrong_session_returns_404(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project(session_id="other-session")
    try:
        resp = client.post(
            f"/api/constructs/{_CONSTRUCT_ID}/digest",
            json={"enzymes": ["EcoRI"]},
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)
    assert resp.status_code == 404


@patch("app.routers.constructs.construct_service.get_construct", new_callable=AsyncMock)
def test_digest_empty_enzyme_list_returns_422(mock_get_construct, client):
    mock_get_construct.return_value = _make_construct()
    _override_db_with_project()
    try:
        resp = client.post(
            f"/api/constructs/{_CONSTRUCT_ID}/digest",
            json={"enzymes": []},
            headers={"X-Session-ID": _SESSION_ID},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)
    assert resp.status_code == 422
