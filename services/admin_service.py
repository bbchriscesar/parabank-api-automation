from requests import Response
from services.base_service import BaseService


class AdminService(BaseService):
    """
    Service Object for administrative database operations.
    Provides methods to initialize and clean the Parabank database.
    """
    CLEAN_DB_ENDPOINT = "/cleanDB"
    INIT_DB_ENDPOINT = "/initializeDB"

    def clean_db(self) -> Response:
        """
        POST /cleanDB
        Resets the database to its default state.
        """
        return self.api_client.post(self.CLEAN_DB_ENDPOINT)

    def initialize_db(self) -> Response:
        """
        POST /initializeDB
        Initializes the database with seed data.
        Used as a session-scoped setup to guarantee deterministic test state.
        """
        return self.api_client.post(self.INIT_DB_ENDPOINT)
