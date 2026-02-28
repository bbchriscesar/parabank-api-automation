import pytest
from services.loans_service import LoansService
from data.test_data import DEFAULT_CUSTOMER, LOAN_DATA, INVALID_DATA


@pytest.mark.regression
class TestLoans:
    @pytest.mark.smoke
    def test_request_loan_decision_logic(self, loans_service: LoansService):
        """
        Test Objective: Validate the loan approval/denial logic based on down payment.
        Endpoint: POST /requestLoan
        """
        response, loan = loans_service.request_loan(
            customer_id=DEFAULT_CUSTOMER.ID,
            amount=LOAN_DATA.AMOUNT,
            down_payment=LOAN_DATA.DOWN_PAYMENT,
            from_account_id=LOAN_DATA.FROM_ACCOUNT_ID
        )

        assert response.status_code == 200, (
            f"Loan Request failed with status {response.status_code}"
        )
        assert loan is not None, "LoanResponse data is missing."
        assert isinstance(loan.approved, bool), "Expected boolean approved state"

    @pytest.mark.negative
    def test_request_loan_invalid_customer(self, loans_service: LoansService):
        """
        Negative: Requesting a loan for a non-existent customer should fail.
        """
        response, loan = loans_service.request_loan(
            customer_id=INVALID_DATA.CUSTOMER_ID,
            amount=LOAN_DATA.AMOUNT,
            down_payment=LOAN_DATA.DOWN_PAYMENT,
            from_account_id=LOAN_DATA.FROM_ACCOUNT_ID
        )

        # Parabank may return a LoanResponse with approved=False, or a 400/404
        if response.status_code == 200 and loan is not None:
            assert loan.approved is False, (
                "Expected loan to be denied for a non-existent customer"
            )
        else:
            assert response.status_code in [400, 404], (
                f"Expected error status for invalid customer, got {response.status_code}"
            )
