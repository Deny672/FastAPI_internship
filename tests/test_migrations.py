from fastapi.testclient import TestClient
from app.main import app
from alembic import command
from alembic.config import Config
from app.core.config import settings

client = TestClient(app)


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

def downgrade_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_DATABASE_URL)
    command.downgrade(alembic_cfg, "base")

def setup_module():
    run_migrations()

def teardown_module():
    downgrade_migrations()

def test_postgres_health_check():
    response = client.get("/healthcheck/test_postgres")
    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "detail": "ok",
        "result": "test_postgres working"
    }
