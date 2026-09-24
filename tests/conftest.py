import pytest
import sqlite3
from fastapi.testclient import TestClient
import app.main as app_main

fastapi_instance = app_main.app 

# Use a named shared cache format so that separate connections can see the same tables
TEST_DB_URI = "file:test_ecommerce?mode=memory&cache=shared"

@pytest.fixture(autouse=True)
def setup_test_database(monkeypatch):
    """Overrides the database connection factory to use a shared in-memory DB securely."""
    
    # 1. Establish a persistent controller connection to keep the shared memory space alive
    base_conn = sqlite3.connect(TEST_DB_URI, uri=True)
    
    # 2. Define a safe factory method that endpoints can call from any thread
    def mock_get_db_connection():
        conn = sqlite3.connect(TEST_DB_URI, uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    # 3. Apply the patch across all core internal systems
    import app.database
    import app.routers.auth
    import app.routers.browsing
    import app.routers.cart
    import app.auth

    monkeypatch.setattr(app.database, "get_db_connection", mock_get_db_connection)
    monkeypatch.setattr(app.routers.auth, "get_db_connection", mock_get_db_connection)
    monkeypatch.setattr(app.routers.browsing, "get_db_connection", mock_get_db_connection)
    monkeypatch.setattr(app.routers.cart, "get_db_connection", mock_get_db_connection)
    monkeypatch.setattr(app.auth, "get_db_connection", mock_get_db_connection)
    
    # 4. Spin up target tables inside the temporary memory block
    app.database.init_db()
    
    yield base_conn
    
    # Close down memory pool blocks after execution finishes
    base_conn.close()

@pytest.fixture
def client():
    """Provides a fresh TestClient pointing directly to the callable FastAPI instance."""
    with TestClient(fastapi_instance) as test_client:
        yield test_client
