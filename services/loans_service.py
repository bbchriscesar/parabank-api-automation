from requests import Response
from services.base_service import BaseService
from models.loan import LoanResponse
from typing import Optional, Tuple


class LoansService(BaseService):
    """
    Service Object for Loan request operations.
    Encapsulates the /requestLoan endpoint.
    """
    REQUEST_LOAN_ENDPOINT = "/requestLoan"

    def request_loan(self, customer_id: int, amount: float, down_payment: float, from_account_id: int) -> Tuple[Response, Optional[LoanResponse]]:
        """
        POST /requestLoan
        Submits a loan request for approval.
        """
        params = {
            "customerId": customer_id,
            "amount": amount,
            "downPayment": down_payment,
            "fromAccountId": from_account_id
        }
        response = self.api_client.post(self.REQUEST_LOAN_ENDPOINT, params=params)
        loan = None
        if response.status_code == 200:
            loan = LoanResponse.model_validate(response.json())
        return response, loan
