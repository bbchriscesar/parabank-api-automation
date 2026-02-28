"""
Centralized test data constants for the Parabank API test suite.

Using dataclasses to group related test data logically, avoiding magic numbers
and hardcoded values scattered across test files.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DefaultCustomer:
    """Known default customer seeded in Parabank's database (John Smith)."""
    ID: int = 12212
    FIRST_NAME: str = "John"
    LAST_NAME: str = "Smith"


@dataclass(frozen=True)
class DefaultCredentials:
    """Default demo login credentials for Parabank."""
    USERNAME: str = "john"
    PASSWORD: str = "demo"


@dataclass(frozen=True)
class InvalidCredentials:
    """Credentials that should always fail authentication."""
    USERNAME: str = "nonexistent_user_xyz"
    PASSWORD: str = "wrong_password_123"


@dataclass(frozen=True)
class AccountData:
    """Known account IDs and test parameters for account operations."""
    # Parabank seeds this account on initialization
    DEFAULT_ID: int = 12345
    SECONDARY_ID: int = 54321
    TRANSFER_AMOUNT: float = 100.00
    OVERDRAFT_AMOUNT: float = 999999.99
    NEGATIVE_AMOUNT: float = -50.00
    NEW_ACCOUNT_TYPE_SAVINGS: int = 1
    NEW_ACCOUNT_TYPE_CHECKING: int = 0


@dataclass(frozen=True)
class InvalidData:
    """Data values expected to trigger error responses."""
    CUSTOMER_ID: int = 999999
    ACCOUNT_ID: int = 999999


@dataclass(frozen=True)
class LoanData:
    """Test parameters for loan request operations."""
    AMOUNT: float = 10000.00
    DOWN_PAYMENT: float = 100.00
    FROM_ACCOUNT_ID: int = 12345


@dataclass(frozen=True)
class TransactionDateRange:
    """Date range parameters for transaction filtering tests."""
    FROM_DATE: str = "01-01-2023"
    TO_DATE: str = "12-31-2023"


# Singleton instances for easy import
DEFAULT_CUSTOMER = DefaultCustomer()
DEFAULT_CREDENTIALS = DefaultCredentials()
INVALID_CREDENTIALS = InvalidCredentials()
ACCOUNT_DATA = AccountData()
INVALID_DATA = InvalidData()
LOAN_DATA = LoanData()
TRANSACTION_DATES = TransactionDateRange()
