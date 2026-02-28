import pytest
from services.customers_service import CustomersService
from data.test_data import DEFAULT_CUSTOMER, INVALID_DATA


@pytest.mark.smoke
class TestCustomers:
    def test_get_customer_success(self, customers_service: CustomersService):
        """
        Verify that we can retrieve a customer by ID and that
        the response schema conforms to our Pydantic model.
        """
        response, customer = customers_service.get_customer(DEFAULT_CUSTOMER.ID)

        # 1. Validate Status Code
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

        # 2. Validate Response Schema (implicitly passed via Pydantic validation)
        assert customer is not None, "Customer data is missing."

        # 3. Validate specific business values
        assert customer.id == DEFAULT_CUSTOMER.ID, (
            f"Expected customer ID {DEFAULT_CUSTOMER.ID}, got {customer.id}"
        )
        assert customer.firstName == DEFAULT_CUSTOMER.FIRST_NAME, (
            f"Expected {DEFAULT_CUSTOMER.FIRST_NAME}, got {customer.firstName}"
        )
        assert customer.lastName == DEFAULT_CUSTOMER.LAST_NAME, (
            f"Expected {DEFAULT_CUSTOMER.LAST_NAME}, got {customer.lastName}"
        )

    @pytest.mark.negative
    def test_get_customer_not_found(self, customers_service: CustomersService):
        """
        Verify that requesting a non-existent customer returns an appropriate error.
        Parabank returns 400 for generic exceptions on missing resources.
        """
        response, customer = customers_service.get_customer(INVALID_DATA.CUSTOMER_ID)

        assert response.status_code in [400, 404], (
            f"Expected 400/404 for invalid customer, got {response.status_code}"
        )
        assert customer is None, "Did not expect customer data for an invalid ID"
