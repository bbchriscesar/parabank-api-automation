from requests import Response
from services.base_service import BaseService
from models.customer import Customer
from typing import Optional, Tuple


class AuthService(BaseService):
    """
    Service Object for Authentication operations.
    Handles Login workflows via the Parabank REST API.
    """
    LOGIN_ENDPOINT = "/login"

    def login(self, username: str, password: str) -> Tuple[Response, Optional[Customer]]:
        """
        Login using credentials.
        Endpoint: GET /login/{username}/{password}
        """
        response = self.api_client.get(f"{self.LOGIN_ENDPOINT}/{username}/{password}")
        customer = None
        if response.status_code == 200:
            customer = Customer.model_validate(response.json())
        return response, customer
