from typing import Any

import requests


class CurrencyHandler:
    def __init__(self, base_currency: str = "usd"):
        # You can only use "usd" as base in the API when using free tier.
        # Feel free to add more parameters if you have ideas on how
        # the class might benefit from that, making it more customizable.
        """
        Initialize the CurrencyHandler.

        This constructor should:
        1. Attempt to load currency data from a JSON file using the load_currency_data method.
        2. If no JSON data is found or if it's outdated, fetch new data from the exchangerates API using the fetch_currency_data method.
        3. Initialize any necessary instance variables for storing currency data and API information.

        # ADVICE: Start implementing the fetch_currency_data method
        """
        pass

    def fetch_currency_data(self) -> dict[str, Any]:
        """
        Fetch the latest currency exchange rate data from the openexchangerates API.

        This method should:
        1. Make an API request to fetch the latest exchange rates.
        2. Parse the JSON response and extract relevant data.
        3. Store the fetched data in the appropriate instance variable(s).
        4. Handle any potential errors or exceptions that may occur during the API request.

        Returns:
            A dictionary containing the latest exchange rates and metadata.
        """
        # Use this code to fetch currency data from openexchangerates.org.
        app_id = "YOUR_APP_ID"  # Add your own app_id from openexchangerates.org here
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}"
        headers = {
            "accept": "application/json"
        }  # This needs to be added, it tells the API that they should return JSON
        response = requests.get(url, headers=headers)
        # Implement the rest of the method
        pass

    def convert_from_usd(self, to_currency: str, amount: float) -> float:
        """
        Convert a given amount from USD to another specified currency.
        This does not require you to use a "base" in the API, it can be done using basic math.

        Args:
            to_currency: The 3-letter code of the currency to convert to.
            amount: The amount in USD to be converted.

        Returns:
            The converted amount in the specified currency.

        Raises:
            ValueError: If the currency code is invalid or the amount is negative.
        """
        pass

    def convert_any_currency(
        self, from_currency: str, to_currency: str, amount: float
    ) -> float:
        """
        Convert an amount from one currency to another using the latest exchange rates.

        Args:
            from_currency: The 3-letter code of the currency to convert from.
            to_currency: The 3-letter code of the currency to convert to.
            amount: The amount to be converted.

        Returns:
            The converted amount in the target currency.

        Raises:
            ValueError: If either currency code is invalid or the amount is negative.
        """
        pass

    def list_currencies(self) -> list[str]:
        """
        List all available currencies in alphabetical order.
        # BONUS - somehow get the full currency names, and include that as well. Feel free to do it any way you like.

        Returns:
            A sorted list of available currency codes.
        """
        pass

    def load_currency_data(self) -> dict[str, Any]:
        """
        Load currency data from a JSON file.

        This method should:
        1. Check if a JSON file with saved currency data exists.
        2. If it exists, read and parse the JSON data.
        3. Check the timestamp of the saved data.
        4. If the data is older than one hour, call fetch_currency_data to update it.
        5. If no file exists or there's an error reading it, call fetch_currency_data.

        Returns:
            A dictionary containing the loaded (or fetched) currency data.
        """
        pass

    def export_to_json(self) -> None:
        """
        Export the current currency data (for the latest currencies) to a JSON file.

        This method should:
        1. Convert the current currency data into a JSON-formatted string.
        2. Write the JSON data to a file, including the current timestamp.
        3. Handle potential errors that may occur during file writing.

        Raises:
            IOError: If there's an error writing to the file, or a custom exception.
        """
        pass

    def get_historical_rate(self, date: str, base_currency: str) -> dict[str, Any]:
        """
        Get the historical exchange rate for a specific date using
        one of the relevant API-endpoints.

        Args:
            date: Date in YYYY-MM-DD format
            base_currency: 3-letter currency code to fetch historical rates based on

        Returns:
            The historical exchange rates as a dictionary for a specific date
            You should probably store it in a list or dict.
        """
        pass

    def list_historical_rates_for_currency(
        self, currency: str, days: int
    ) -> list[tuple[str, str]]:
        """
        Get the trend of exchange rates for a currency over a specified number of days.

        Args:
            currency: 3-letter currency code
            days: Number of days to look back

        Returns:
            A list of tuples, each containing a date and the corresponding rate
            Tuples are typically used to store pairs of values.
        """
        pass
