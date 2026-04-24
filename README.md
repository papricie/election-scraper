# Election scraper

A Python CLI application for scraping Czech election results.

## About the project

This project automates the extraction of 2017 Czech Parliamentary Election results from the official volby.cz website. It scrapes data from district pages, processes individual municipality results, and saves them to CSV format for analysis.

The focus is on robust web scraping, input validation, error handling, and comprehensive testing to ensure reliability.

---

## Tech stack

- Python 3.x
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP requests)
- Pytest (unit testing)
- CSV (data export)

---

## Project structure

```
election-scraper/
│
├── scraper/
│   ├── __init__.py
│   ├── main.py          # CLI logic and orchestration
│   ├── logic.py         # Web scraping and data parsing
│   └── utils.py         # URL validation utilities
│
├── tests/
│   ├── test_logic.py    # Unit tests for scraping logic
│   └── test_utils.py    # Unit tests for validation
│
├── main.py              # CLI entry point
├── requirements.txt     # Dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

## Installation

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

Run the scraper with a district URL and destination CSV file:

```powershell
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" output.csv
```

## Testing

The project includes comprehensive unit tests to ensure code quality and prevent regressions.

### How to run tests

Run all tests using:

```bash
python -m pytest -v
```

Or for quiet output:

```bash
python -m pytest -q
```

### Test coverage

#### `tests/test_logic.py`

- **`test_get_municipality_links`**: Tests the extraction of municipality links from a district page HTML. Uses mocked HTTP responses to verify that links and names are correctly parsed without making real network calls.

- **`test_parse_obec`**: Tests parsing of election data from a single municipality page. Mocks the HTTP response and checks that voter counts, ballot counts, valid votes, and party results are accurately extracted.

#### `tests/test_utils.py`

- **`test_validate_url_accepts_volby_url`**: Verifies that the URL validation function accepts valid volby.cz URLs, ensuring the scraper only processes authorized sources.

- **`test_validate_url_rejects_other_url`**: Ensures the validation rejects invalid or external URLs, protecting against misuse and potential security issues.

These tests use mocking to isolate logic from external dependencies, making them fast and reliable. They cover happy paths and basic validation scenarios.

## Improvements

- Add retry/backoff for network requests
- Add argument to adjust request pacing
- Add JSON or SQLite export option
- Add GitHub Actions workflow for CI
- Add integration tests using a sandboxed HTML fixture
