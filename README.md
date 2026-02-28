# Parabank API Automation Framework

A robust, scalable API test automation framework for testing the [Parabank API](https://parabank.parasoft.com/parabank/api-docs/index.html). Built using Python, `pytest`, `requests`, and `pydantic`.

## Features
- **Service Object Model**: API-adapted Page Object Model pattern with `BaseService` abstraction for DRY service layers.
- **API Client Wrapper**: A customized `requests.Session` client with configurable timeouts, automatic retry logic for transient failures, structured logging, and custom exceptions.
- **Pydantic Validation**: Strict schema validation using Pydantic models for API responses.
- **Environment Management**: Type-safe environment variables handling with `pydantic-settings` (e.g., using `.env` files).
- **Test Data Management**: Centralized, frozen dataclass-based test constants — no magic numbers in tests.
- **Deterministic Test Setup**: Auto-use `db_setup` fixture initializes the database before every test session.
- **Custom Markers**: `smoke`, `regression`, and `negative` markers for selective test execution.
- **Test Reporting**: Automatic generation of HTML reports (`pytest-html`).

## Project Structure
```text
parabank-api-automation/
├── config/                 # Settings and configurations (pydantic-settings)
│   ├── __init__.py
│   └── settings.py
├── core/                   # Low-level wrappers and utilities
│   ├── __init__.py
│   ├── api_client.py       # Wrapper around requests.Session (timeout + retry)
│   └── exceptions.py       # Custom API exception classes
├── data/                   # Centralized test data constants
│   ├── __init__.py
│   └── test_data.py        # Frozen dataclasses for test parameters
├── fixtures/               # Pytest fixtures for dependency injection
│   ├── __init__.py
│   ├── api_client_fixture.py
│   └── services_fixtures.py  # Service fixtures + db_setup autouse fixture
├── models/                 # Pydantic schema models for response validation
│   ├── __init__.py
│   ├── account.py
│   ├── customer.py
│   ├── loan.py
│   └── transaction.py
├── services/               # Service Objects (API Object Model pattern)
│   ├── __init__.py
│   ├── base_service.py     # Abstract base service class
│   ├── accounts_service.py
│   ├── admin_service.py
│   ├── auth_service.py
│   ├── customers_service.py
│   └── loans_service.py
├── tests/                  # Test suites with markers
│   ├── __init__.py
│   ├── test_accounts.py    # Smoke + Regression + Negative
│   ├── test_admin.py       # Regression
│   ├── test_auth.py        # Smoke + Negative
│   ├── test_customers.py   # Smoke + Negative
│   └── test_loans.py       # Regression + Negative
├── conftest.py             # Root-level fixture plugin registration
├── pytest.ini              # Pytest configuration with custom markers
├── requirements.txt        # Python package dependencies
├── openapi.yaml            # Parabank API specification
├── .env                    # Local environment variables (gitignored)
└── .env.example            # Example environment variables template
```

## Prerequisites
- Python 3.10+
- `pip` package manager

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd parabank-api-automation
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the `.env.example` file to create your own local `.env` file:
   ```bash
   cp .env.example .env
   ```

## Running the Tests

### Full Suite
```bash
pytest tests/
```

### By Marker
Run only smoke (critical path) tests:
```bash
pytest tests/ -m smoke
```

Run only negative / edge case tests:
```bash
pytest tests/ -m negative
```

Run the full regression suite:
```bash
pytest tests/ -m regression
```

### Viewing Test Reports
After executing pytest, an HTML test report is automatically generated at `report.html`.
Open it in your browser to view detailed logs and test summaries.

## Writing Tests

1. **Define your validation models**: Create a Pydantic `BaseModel` class in `models/` for the expected API response.
2. **Add test data**: Add constants to `data/test_data.py` as frozen dataclasses.
3. **Create or extend a Service**: Add methods to the relevant service in `services/` (inheriting `BaseService`).
4. **Write your test**: Use fixtures and centralized test data, apply markers.

```python
import pytest
from services.customers_service import CustomersService
from data.test_data import DEFAULT_CUSTOMER

@pytest.mark.smoke
def test_example(customers_service: CustomersService):
    response, customer = customers_service.get_customer(DEFAULT_CUSTOMER.ID)
    assert response.status_code == 200

    assert customer is not None
    assert customer.firstName == DEFAULT_CUSTOMER.FIRST_NAME
```
