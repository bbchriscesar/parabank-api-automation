import pytest
from services.auth_service import AuthService
from data.test_data import DEFAULT_CREDENTIALS, INVALID_CREDENTIALS, DEFAULT_CUSTOMER


@pytest.mark.smoke
class TestAuthAndRegistration:
    def test_login_success(self, auth_service: AuthService):
        """
        Verify that a user can successfully log in using valid credentials.
        The Parabank default demo credentials are john / demo.
        """
        login_response, customer = auth_service.login(
            username=DEFAULT_CREDENTIALS.USERNAME,
            password=DEFAULT_CREDENTIALS.PASSWORD
        )

        # 1. Validate Status Code
        assert login_response.status_code == 200, (
            f"Login failed: Expected 200, got {login_response.status_code}"
        )

        # 2. Validate Response Schema (implicitly via Pydantic)
        assert customer is not None, "Customer login response data is missing."

        # 3. Validate specific business context
        assert customer.firstName == DEFAULT_CUSTOMER.FIRST_NAME, (
            f"Expected {DEFAULT_CUSTOMER.FIRST_NAME}, got {customer.firstName}"
        )
        assert customer.lastName == DEFAULT_CUSTOMER.LAST_NAME, (
            f"Expected {DEFAULT_CUSTOMER.LAST_NAME}, got {customer.lastName}"
        )

    @pytest.mark.negative
    def test_login_invalid_credentials(self, auth_service: AuthService):
        """
        Negative: Verify that login with wrong credentials returns an error.
        """
        login_response, customer = auth_service.login(
            username=INVALID_CREDENTIALS.USERNAME,
            password=INVALID_CREDENTIALS.PASSWORD
        )

        assert login_response.status_code in [400, 401, 403], (
            f"Expected authentication error status, got {login_response.status_code}"
        )
        assert customer is None, "Did not expect customer data for invalid credentials"
