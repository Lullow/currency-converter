# Currency Converter

A terminal-based currency conversion app built in Python, using the OpenExchangeRates API.

This was my **second Python lab**, built during the course *Programmering i Python* in October 2025. The focus was on object-oriented programming — building a reusable class that handles all currency logic, separate from the UI in `main.py`.

## What it does

- List all available currencies
- Convert USD to any currency
- Convert between any two currencies
- Fetch and refresh live exchange rate data from the API
- Export rate data to JSON
- Look up historical exchange rates by date
- View rate trends for a currency over a chosen number of days

## How to run

```bash
pip install -r requirements.txt
python main.py
```

Requires a free API key from [openexchangerates.org](https://openexchangerates.org/).

## Structure

- `main.py` — menu and user interaction
- `currencyhandler.py` — `CurrencyHandler` class with all currency logic
- `requirements.txt` — dependencies
- `updated_rates.json` — cached rate data

## Tech

- Python 3
- `requests` library
- OpenExchangeRates API
