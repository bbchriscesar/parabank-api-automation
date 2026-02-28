from requests import Response
from services.base_service import BaseService
from models.customer import Customer
from typing import Optional, Tuple


class CustomersService(BaseService):
    """
    Service Object for the Customers endpoint.
    Encapsulates all actions related to /customers.
    """
    endpoint = "/customers"

    def get_customer(self, customer_id: int | str) -> Tuple[Response, Optional[Customer]]:
        """Fetch a customer by their unique ID."""
        response = self.api_client.get(f"{self.endpoint}/{customer_id}")
        customer = None
        if response.status_code == 200:
            customer = Customer.model_validate(response.json())
        return response, customer
