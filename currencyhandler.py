import json
import os  # Needed for reading the API key from the environment.
from datetime import (  # Needed for calculating date and time.
    datetime,
    timedelta,
    timezone,
)
from typing import Any

import requests
from dotenv import load_dotenv  # loads environment variables from .env file

load_dotenv(override=True)      # ensure that .env values has higher priority over system values


class CurrencyHandler:
    def __init__(self, base_currency: str = "usd"):
        # You can only use "usd" as base in the API when using free tier.
        # Feel free to add more parameters if you have ideas on how.
        # the class might benefit from that, making it more customizable.
        """
        Initialize the CurrencyHandler.

        This constructor should:
        1. Attempt to load currency data from a JSON file using the load_currency_data method.
        2. If no JSON data is found or if it's outdated, fetch new data from the exchangerates API using the fetch_currency_data method.
        3. Initialize any necessary instance variables for storing currency data and API information.

        # ADVICE: Start implementing the fetch_currency_data method
        """
        # For storing the base currency and converting string to uppercase-letters.
        self.base = base_currency.upper()
        # Store the API data.
        self.data = {}
        # Store the rates for currency.
        self.rates = {}
        # placeholder.
        self.timestamp = None
        # The API key is read from the environment, never stored in the code.
        self.app_id = os.getenv("OXR_APP_ID")
        if not self.app_id:
            raise RuntimeError(
                "Missing OXR_APP_ID. Create a .env file with your key from "
                "openexchangerates.org, see .env.example."
            )

        try:
            self.fetch_currency_data()
        except Exception as e:
            # Raises a description of what type of error occured.
            raise RuntimeError(f"Failed to initialize Currencyhandler: {e}")



    def list_rates(self):
        """Return a list contaning all currencies in alphabetical order"""
        # Handle possible crasch if self.rates dict is empty by returning an empty list.
        if not self.rates:
            return []

        # If dict contains data - return it sorted by alphabetical order.
        # keys() used for getting only keys else we get key:values in dict style{}
        return sorted(self.rates.keys()) 



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
        url = f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}"
        # This needs to be added, it tells the API that they should return JSON.
        headers = {"accept": "application/json"}
        

        try: 
            # Send the request to the server, pass-in a timeout at 10 seconds or it will run indefinitely.
            response = requests.get(url, headers=headers, timeout=10)

            # Raises HTTPError for codes  like 404, 500.
            response.raise_for_status()
            # Convert data to a .json, then into a dict and store it in variable "data".
            data: dict[str, Any] = response.json()
            # Self.data saves the "whole" JSON response.
            self.data = data
            # Looks for the value (every currency) from data - print a default value "{}" if "rates" does not exist-
            self.rates = data.get("rates", {})
            # Because USD is the only base we can work with. / .get requests the data from server (the base currency in this case)-
            self.base = data.get("base", "USD")
            # Saves the last time data was timestamped (updated) / .get requests the data from server (the timestamp in this case).
            self.timestamp = data.get("timestamp")
            # Returns data
            return data
        
        # Exceptions: Timeout error, connection error, HTTP error and unexcpected errors:
        except requests.exceptions.Timeout:
            raise TimeoutError("The request timed out, Try again later.")        
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Could not connect, check your internetconncetion.")        
        except requests.HTTPError as e:
            raise RuntimeError(f"HTTP error: {e}")        
        except Exception as e:
            raise(f"There was an unexpected error: {e}" )
        



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

        # amount: The amount in USD to be converted.
        # Basic errorhandling.
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        # to_currency: The 3-letter code of the currency to convert to.
        # Set all currencies to upper-letter str, and accept extra spaces.
        convert_currency = to_currency.strip().upper()

        # List of rates that we fetched eairlier.
        # Raise ValueError if currency not in list.
        if convert_currency not in self.rates:
            raise ValueError(f"No such currency found: {convert_currency}")
        
        # Use self.rate becase it's the dict that stores the live dict.
        # Create variable rate, get value from to_currency key.
        # This mean basically self.rate["SEK"] if we convert from USD -> SEK.
        # So it will look up SEK in rates and return the value example: 1 USD -> 10.50 SEK.
        # Rate stores the value (rate = (SEK)10.50)).
        # Convert to float-type.
        # Return the amount times the rate ("1usd * 10.50sek = 10.50 SEK")
        rate = float(self.rates[convert_currency])
        return amount * rate



    def convert_any_currency(
        self, from_currency: str, to_currency: str, amount: float) -> float:
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


        # Create two variables to work with, uppsercase and strip them for better UI.
        convert_from = from_currency.upper().strip()
        convert_to = to_currency.upper().strip()

        # Basic errorhandling for currency code (check that both codes exists in the rate dict).
        if amount <= 0 or convert_from not in self.rates or convert_to not in self.rates:
            raise ValueError ("Invalid input, check amount or currency codes.")

        # Get exchange rate from currencies.
        # from_rate: rate for the currency converted FROM
        # to_rate rate for the currency converted TO 
        from_rate = self.rates[convert_from]
        to_rate = self.rates[convert_to]

        # Convert the amount from the choosen rate to USD.
        base_amount = amount / from_rate
        # Convert the base amount (USD) to choosen rate.
        converted_amount = base_amount * to_rate

        # Return the evaluated result
        return converted_amount



    # Created list_rates method do handle this functionallity-
    def list_currencies(self) -> list[str]:
        """
        Returns: A sorted list of available currency codes. 
        """



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


    # self.data contains all the data we imported from the site
    # Create new parameter and set it to string "updated_rates.json" to use in menuchoice.
    def export_to_json(self, filename: str = "updated_rates.json") -> None:
        """
        Export the current currency data (for the latest currencies) to a JSON file.

        This method should:
        1. Convert the current currency data into a JSON-formatted string.
        2. Write the JSON data to a file, including the current timestamp.
        3. Handle potential errors that may occur during file writing.

        Raises:
            IOError: If there's an error writing to the file, or a custom exception.
        """
        # If there's no data raise error.
        if not self.data:
            raise ValueError("No data found.")
        

        # Open a file for writing ("w") "w" also creates file if it doesn't exist.
        # Create method parameter "filename" and use it below
        # .dump converts py dict to json string and writes it to the file.
        # indent=number gives a better structure to the exported file, else it will display as a long string with all info.
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)

        except OSError as e:
            # Raise error if something wrong when writing the file.
            raise IOError(f"Failed to export data to file: {filename}: {e}")



    # Change parameter base_currency to USD (free-user only allows USD as base).
    def get_historical_rate(self, date: str, base_currency: str="USD") -> dict[str, Any]:
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

        # Create f-string and variables for URL and date, the app ID comes from the environment.
        url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={self.app_id}"

        try:
            # Create variable and get request for url, add connection timeout at 10 seconds.
            response = requests.get(url, timeout=10)
            # Checks for HTTP status code of the response and raises error if it's not correct.
            response.raise_for_status()
            # Create variable that stores the response as json (historical_data variable will be a dict format due to .json (converts it automatically))
            historical_data = response.json()
        
        # Basic error handling, return empty dict in this case of anything goes wrong.
        except Exception:
            return {}
        
        return historical_data




    def list_historical_rates_for_currency(self, currency: str, days: int) -> list[tuple[str, str]]:
        """
        Get the trend of exchange rates for a currency over a specified number of days.

        Args:
            currency: 3-letter currency code
            days: Number of days to look back

        Returns:
            A list of tuples, each containing a date and the corresponding rate
            Tuples are typically used to store pairs of values.
        """

        if days <= 0:
            raise ValueError("Please enter a positive number.")

        # Store date and rate
        results: list[tuple[str, str]] = []
        user_code = currency.strip().upper()

        # Sets time to UTC / .date() to remove time (only use date). Variable represents todays date in UTC.
        today = datetime.now(timezone.utc).date()

        for i in range(days):
            # Math operation that goes back one day for each iteration.
            prior_day = today - timedelta(days=i)
            # Returns a string representing date.
            date_string = prior_day.strftime("%Y-%m-%d")
            # Reuse historical_rate method (date_string contains timestamp, rates).
            new_data = self.get_historical_rate(date_string)
            # Get rates for target currency and store in rate variable, if not found - store in empty dict to avoid crash
            rate = new_data.get("rates", {}).get(user_code)

            if rate:
                # If rate is found, add it to result and convert it to float (wrap in tuple so it takes two arguments).
                results.append((date_string, float(rate)))
        # Sort the results.
        results.sort()
        # Return the results.
        return results

