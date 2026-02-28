import pytest
from services.customers_service import CustomersService
from models.customer import Customer
from pydantic import ValidationError

class TestCustomers:
    def test_get_customer_success(self, customers_service: CustomersService):
        """
        Verify that we can retrieve a customer by ID and that 
        the response schema conforms to our Pydantic model.
        """
        # A known default customer ID in parabank is 12212 (John Smith)
        customer_id = 12212
        
        # Use the Service Object to get the customer (API Object Model)
        response = customers_service.get_customer(customer_id)
        
        # 1. Validate Status Code
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        
        # 2. Validate Response Schema using Pydantic
        try:
            customer = Customer.model_validate(response.json())
        except ValidationError as e:
            pytest.fail(f"Response schema validation failed:\n{e}")
            
        # 3. Validate specific business values
        assert customer.id == customer_id, f"Expected customer ID {customer_id}, got {customer.id}"
        assert customer.firstName == "John", f"Expected John, got {customer.firstName}"
        assert customer.lastName == "Smith", f"Expected Smith, got {customer.lastName}"
        
    def test_get_customer_not_found(self, customers_service: CustomersService):
        """
        Verify that requesting a non-existent customer returns an appropriate error.
        Parabank usually returns 400 for generic exceptions.
        """
        invalid_id = 999999
        
        # Use the Service Object to get the non-existent customer
        response = customers_service.get_customer(invalid_id)
        
        assert response.status_code == 400, f"Expected 400 for invalid customer, got {response.status_code}"
