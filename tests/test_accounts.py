import pytest
from services.accounts_service import AccountsService
from data.test_data import DEFAULT_CUSTOMER, ACCOUNT_DATA, INVALID_DATA, TRANSACTION_DATES


@pytest.mark.regression
class TestAccounts:
    @pytest.mark.smoke
    def test_get_account_details(self, accounts_service: AccountsService):
        """
        Test Objective: Ensure the API returns the correct account information for a specific ID.
        Endpoint: GET /accounts/{accountId}
        """
        response, account = accounts_service.get_account(ACCOUNT_DATA.DEFAULT_ID)

        assert response.status_code == 200, (
            f"Expected 200 OK, got {response.status_code}. "
            f"Ensure DB is initialized with account {ACCOUNT_DATA.DEFAULT_ID}."
        )
        assert account is not None, "Failed to parse Account data"
        assert account.id == ACCOUNT_DATA.DEFAULT_ID

    def test_fund_transfer_between_accounts(self, accounts_service: AccountsService):
        """
        Test Objective: Verify that funds can be moved from one account to another.
        Endpoint: POST /transfer
        """
        # First, create a second account to ensure a valid target exists
        _, target_account = accounts_service.create_account(
            customer_id=DEFAULT_CUSTOMER.ID,
            new_account_type=ACCOUNT_DATA.NEW_ACCOUNT_TYPE_CHECKING,
            from_account_id=ACCOUNT_DATA.DEFAULT_ID
        )
        assert target_account is not None, "Prerequisite failed: could not create target account."

        response = accounts_service.transfer(
            ACCOUNT_DATA.DEFAULT_ID,
            target_account.id,
            ACCOUNT_DATA.TRANSFER_AMOUNT
        )

        assert response.status_code == 200, (
            f"Transfer failed with status {response.status_code}"
        )

        # Verification: follow-up GET to confirm accounts still accessible
        from_resp, _ = accounts_service.get_account(ACCOUNT_DATA.DEFAULT_ID)
        to_resp, _ = accounts_service.get_account(target_account.id)
        assert from_resp.status_code == 200
        assert to_resp.status_code == 200

    def test_withdraw_funds_boundary(self, accounts_service: AccountsService):
        """
        Test Objective: Check if the system correctly handles a withdrawal
        that exceeds the available balance.
        Endpoint: POST /withdraw

        Note: Parabank's dummy backend has a known flaw where it allows
        infinite overdrafts with a 200 OK. This test documents the defect.
        """
        response = accounts_service.withdraw(ACCOUNT_DATA.DEFAULT_ID, ACCOUNT_DATA.OVERDRAFT_AMOUNT)

        # Document the known defect: Parabank allows overdraft withdrawals
        if response.status_code == 200 and "Insufficient Funds" not in response.text:
            pytest.xfail(
                "Caught defect: Parabank allows overdraft withdrawals "
                "returning 200 OK instead of 400 or Insufficient Funds."
            )

        assert response.status_code == 400 or "Insufficient Funds" in response.text, (
            f"Expected 400 Bad Request, got {response.status_code}"
        )

    @pytest.mark.smoke
    def test_create_new_account(self, accounts_service: AccountsService):
        """
        Test Objective: Verify that a new account can be created for an existing customer.
        Endpoint: POST /createAccount
        """
        response, account = accounts_service.create_account(
            customer_id=DEFAULT_CUSTOMER.ID,
            new_account_type=ACCOUNT_DATA.NEW_ACCOUNT_TYPE_SAVINGS,
            from_account_id=ACCOUNT_DATA.DEFAULT_ID
        )

        assert response.status_code == 200, (
            f"Create Account failed with status {response.status_code}"
        )
        assert account is not None, "Failed to parse Account data"
        assert account.customerId == DEFAULT_CUSTOMER.ID
        assert account.type == "SAVINGS"

    def test_filter_transactions_by_date(self, accounts_service: AccountsService):
        """
        Test Objective: Ensure transactions are correctly filtered within a date range.
        Endpoint: GET /accounts/{accountId}/transactions/fromDate/{fromDate}/toDate/{toDate}
        """
        response, transactions = accounts_service.get_transactions_by_date(
            ACCOUNT_DATA.DEFAULT_ID,
            TRANSACTION_DATES.FROM_DATE,
            TRANSACTION_DATES.TO_DATE
        )

        assert response.status_code == 200, (
            f"Transactions endpoint failed with status {response.status_code}"
        )
        assert transactions is not None, "Failed to parse Transactions data"
        assert isinstance(transactions, list), "Expected a list of transactions"

    @pytest.mark.negative
    def test_get_nonexistent_account(self, accounts_service: AccountsService):
        """
        Negative: Requesting a non-existent account should return an error status.
        """
        response, account = accounts_service.get_account(INVALID_DATA.ACCOUNT_ID)

        assert response.status_code in [400, 404], (
            f"Expected 400/404 for invalid account, got {response.status_code}"
        )
        assert account is None, "Did not expect account data for an invalid ID"

    @pytest.mark.negative
    def test_transfer_negative_amount(self, accounts_service: AccountsService):
        """
        Negative: Transferring a negative amount should be rejected by the API.

        Note: Parabank may allow this (known limitation). If so,
        this test documents the defect via xfail.
        """
        response = accounts_service.transfer(
            ACCOUNT_DATA.DEFAULT_ID,
            ACCOUNT_DATA.DEFAULT_ID,
            ACCOUNT_DATA.NEGATIVE_AMOUNT
        )

        if response.status_code == 200:
            pytest.xfail(
                "Caught defect: Parabank allows negative transfer amounts "
                "without validation."
            )

        assert response.status_code in [400, 422], (
            f"Expected 400/422 for negative amount, got {response.status_code}"
        )
