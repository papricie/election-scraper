# Election scraper

A Python CLI application for scraping Czech election results.

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

## Test

```powershell
pytest
```

## Project structure

- `main.py` — CLI entry point
- `scraper/` — application package
- `tests/` — unit tests
- `requirements.txt` — dependencies

## Improvements

- Add retry/backoff for network requests
- Add argument to adjust request pacing
- Add JSON or SQLite export option
- Add GitHub Actions workflow for CI
- Add integration tests using a sandboxed HTML fixture
