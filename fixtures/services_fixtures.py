import pytest
import logging
from core.api_client import APIClient
from services.customers_service import CustomersService
from services.auth_service import AuthService
from services.accounts_service import AccountsService
from services.loans_service import LoansService
from services.admin_service import AdminService

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def customers_service(api_client: APIClient) -> CustomersService:
    return CustomersService(api_client=api_client)


@pytest.fixture(scope="session")
def auth_service(api_client: APIClient) -> AuthService:
    return AuthService(api_client=api_client)


@pytest.fixture(scope="session")
def accounts_service(api_client: APIClient) -> AccountsService:
    return AccountsService(api_client=api_client)


@pytest.fixture(scope="session")
def loans_service(api_client: APIClient) -> LoansService:
    return LoansService(api_client=api_client)


@pytest.fixture(scope="session")
def admin_service(api_client: APIClient) -> AdminService:
    return AdminService(api_client=api_client)


@pytest.fixture(scope="session", autouse=True)
def db_setup(admin_service: AdminService):
    """
    Session-scoped auto-use fixture that initializes the Parabank database
    before any tests run. This guarantees deterministic test state and
    eliminates the need for pytest.skip() fallbacks.
    """
    logger.info("Initializing Parabank database for test session...")
    response = admin_service.initialize_db()
    assert response.status_code in [200, 204], (
        f"Failed to initialize database. Status: {response.status_code}"
    )
    logger.info("Database initialized successfully.")
    yield
    # Optional: clean up after the entire session
    logger.info("Test session complete.")
