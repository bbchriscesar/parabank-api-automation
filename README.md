# Parabank API Automation Framework

A robust, scalable API test automation framework for testing the [Parabank API](https://parabank.parasoft.com/parabank/api-docs/index.html). Built using Python, `pytest`, `requests`, and `pydantic`.

## Features
- **Modular Design**: Core client, configurations, models, and tests are neatly separated.
- **API Client Wrapper**: A customized `requests.Session` client logging requests and responses, and handling HTTP interactions.
- **Pydantic Validation**: Strict schema validation using Pydantic models for API responses.
- **Environment Management**: Robust environment variables handling with `pydantic-settings` (e.g., using `.env` files).
- **Test Reporting**: Automatic generation of HTML reports (`pytest-html`) mapping test execution to visually understandable results.

## Project Structure
```text
parabank-api-automation/
├── config/             # Settings and configurations (pydantic-settings)
│   └── settings.py
├── core/               # Low-level wrappers and utilities
│   └── api_client.py   # Wrapper around requests.Session
├── data/               # Test data files (JSON, YAML, CSV)
├── fixtures/           # Pytest fixtures to inject dependencies
│   └── api_client_fixture.py
├── models/             # Pydantic schema models for response validation
│   └── customer.py
├── tests/              # The actual test suites
│   ├── __init__.py
│   └── test_customers.py 
├── conftest.py         # Root level fixture definitions
├── pytest.ini          # Pytest configuration file
├── requirements.txt    # Python package dependencies
├── .env                # Local environment variables
└── .env.example        # Example environment variables template
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
   Copy the `.env.example` file to create your own local `.env` file. You can override the Base URL and other configurations here.
   ```bash
   cp .env.example .env
   ```

## Running the Tests

To run the entire suite of tests, execute:
```bash
pytest tests/
```

### Viewing Test Reports
After executing pytest, an HTML test report is automatically generated at the run execution folder root: `report.html`.
Simply open `report.html` in your favorite web browser to view detailed logs and test summaries.

## Writing Tests
1. **Define your validation models**: Create a new class extending `BaseModel` from `pydantic` in the `models/` directory for the expected API response.
2. **Utilize Fixtures**: Add parameters for fixtures (e.g., `api_client`) directly in your test function signatures.
3. **Write assertions**: Assert on status codes, and load the response JSON into your Pydantic validation model.

```python
from models.customer import Customer

def test_example(api_client):
    response = api_client.get("/customers/12212")
    assert response.status_code == 200
    
    # Validates response payload schema strictly!
    data = Customer.model_validate(response.json())
    assert data.firstName == "John"
```
