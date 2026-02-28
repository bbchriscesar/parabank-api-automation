from core.api_client import APIClient
from requests import Response

class CustomersService:
    """
    API Object Model (Service Object) for the Customers endpoint.
    This encapsulates all actions related to /customers.
    """
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.endpoint = "/customers"

    def get_customer(self, customer_id: int | str) -> Response:
        """
        Fetch a customer by their unique ID.
        """
        return self.api_client.get(f"{self.endpoint}/{customer_id}")
