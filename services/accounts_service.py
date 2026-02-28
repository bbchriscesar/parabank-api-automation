from requests import Response
from services.base_service import BaseService
from models.account import Account
from models.transaction import Transaction
from typing import Optional, Tuple, List


class AccountsService(BaseService):
    """
    Service Object for Account-related API operations.
    Encapsulates all endpoints for accounts, transfers, withdrawals, and transactions.
    """
    endpoint = "/accounts"

    # Endpoint constants for non-resource operations
    TRANSFER_ENDPOINT = "/transfer"
    WITHDRAW_ENDPOINT = "/withdraw"
    CREATE_ACCOUNT_ENDPOINT = "/createAccount"

    def get_account(self, account_id: int) -> Tuple[Response, Optional[Account]]:
        """GET /accounts/{accountId}"""
        response = self.api_client.get(f"{self.endpoint}/{account_id}")
        account = None
        if response.status_code == 200:
            account = Account.model_validate(response.json())
        return response, account

    def transfer(self, from_account_id: int, to_account_id: int, amount: float) -> Response:
        """
        POST /transfer
        Moves funds from one account to another.
        """
        params = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": amount
        }
        return self.api_client.post(self.TRANSFER_ENDPOINT, params=params)

    def withdraw(self, account_id: int, amount: float) -> Response:
        """
        POST /withdraw
        Withdraws a specific amount from an account.
        """
        params = {
            "accountId": account_id,
            "amount": amount
        }
        return self.api_client.post(self.WITHDRAW_ENDPOINT, params=params)

    def create_account(self, customer_id: int, new_account_type: int, from_account_id: int) -> Tuple[Response, Optional[Account]]:
        """
        POST /createAccount
        Account types: 0 (CHECKING), 1 (SAVINGS), 2 (LOAN)
        """
        params = {
            "customerId": customer_id,
            "newAccountType": new_account_type,
            "fromAccountId": from_account_id
        }
        response = self.api_client.post(self.CREATE_ACCOUNT_ENDPOINT, params=params)
        account = None
        if response.status_code == 200:
            account = Account.model_validate(response.json())
        return response, account

    def get_transactions_by_date(self, account_id: int, from_date: str, to_date: str) -> Tuple[Response, Optional[List[Transaction]]]:
        """GET /accounts/{accountId}/transactions/fromDate/{fromDate}/toDate/{toDate}"""
        response = self.api_client.get(
            f"{self.endpoint}/{account_id}/transactions/fromDate/{from_date}/toDate/{to_date}"
        )
        transactions = None
        if response.status_code == 200:
            transactions = [Transaction.model_validate(tx) for tx in response.json()]
        return response, transactions
