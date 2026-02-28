import pytest
from services.admin_service import AdminService
from services.customers_service import CustomersService
from data.test_data import INVALID_DATA


@pytest.mark.regression
class TestAdministration:
    def test_database_cleanup(self, admin_service: AdminService, customers_service: CustomersService):
        """
        Test Objective: Ensure the administrative function to reset the database works correctly.
        Endpoint: POST /cleanDB
        """
        # 1. Clean the DB
        response = admin_service.clean_db()

        # Expect successful clean or No Content
        assert response.status_code in [200, 204], (
            f"Clean DB failed, status {response.status_code}"
        )

        # 2. Verify Database is operating by requesting a guaranteed-missing ID
        cust_response, cust = customers_service.get_customer(INVALID_DATA.CUSTOMER_ID)
        assert cust_response.status_code in [400, 404]

        # 3. Re-initialize DB so subsequent tests have deterministic state
        init_response = admin_service.initialize_db()
        assert init_response.status_code in [200, 204], (
            f"Re-initialization failed, status {init_response.status_code}"
        )
