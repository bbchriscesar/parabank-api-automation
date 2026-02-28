import pytest
from core.api_client import APIClient
from services.customers_service import CustomersService

@pytest.fixture(scope="session")
def customers_service(api_client: APIClient) -> CustomersService:
    """
    Fixture to provide an instance of CustomersService to the tests.
    Depends on the `api_client` fixture.
    """
    return CustomersService(api_client=api_client)
