import os
import pytest
from src.app import create_app


@pytest.fixture()
def client():
    # Celowo ustawiamy DATABASE_URL na nieistniejący serwer,
    # żeby testy NIE wymagały uruchomionej bazy na etapie build (Docker test stage).
    os.environ["DATABASE_URL"] = "postgresql+psycopg2://x:y@127.0.0.1:9999/nodb"

    app = create_app()
    app.testing = True
    return app.test_client()


def test_unit_like_logic_version_default(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.get_json()["version"] == "dev"


def test_http_health_returns_json(client):
    resp = client.get("/health")
    assert resp.is_json is True
    data = resp.get_json()
    assert "status" in data
    assert "db" in data


def test_users_route_is_registered(client):
    # Nie wywołujemy /users (bo wymaga DB).
    # Sprawdzamy tylko, czy routing jest zarejestrowany.
    rules = [r.rule for r in client.application.url_map.iter_rules()]
    assert "/users" in rules
