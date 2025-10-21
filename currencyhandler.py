import json
from datetime import (  # Needed for calculating date and time.
    datetime,
    timedelta,
    timezone,
)
from typing import Any

import requests


# CAN I IMPLEMENT CHOICE 0 NOW? YES / NO? - YES BUT NEEDS IMPROVMENTS
# LINE 84 RUNS AS SOON AS PROGRAM STARTS - GOOD / BAD IDEA? 
# IT'S A BAD IDEA - NO PRINTS ONLY RETURNS AS INSTRUCTED! - FIX LATER
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
        self.base = base_currency.upper() # For storing the base currency and converting string to uppercase-letters.
        self.data = {} # Store the API data - THIS IS WHERE ALL DATA IS STORED NOW! USE THIS IN OTHER METHODS TO GET INFORMATION TO THEM
        self.rates = {} # Store the rates for currency 
        self.timestamp = None # placeholder (DONT KNOW WHAT TO DO WITH THIS YET)

        # TRY EXCEPT HERE? OFC - BUT WHAT? DO I NEED TO BE SPECIFIC OR JUST GENERALL MSG?
        self.fetch_currency_data() 

        # ----------------------------------------------

        # !!!!!!!!!!!THIS MUST BE IN ANOTHER METHOD!!!!!!!!!!!!

        # Handle possible crasch if self.rates dict is empty by returning an empty list.
        # if not self.rates: 
        #     return []

        # # If dict contains data - return it sorted by alphabetical order. 
        # # keys() used for getting only keys else we get key:values in dict stryle{}        
        # return sorted(self.rates.keys()) 

        # # - IMPROVISING - IF STATEMENT ABOVE WORKS BETTER THAN CODE BELOW.. I THINK..? DONT DELITE JUST YET.
        # self.rates = list(self.rates.keys()) # Return all rates and store it in variable "self.rates"
        # self.rates = sorted(self.rates) # Sort them in alphabetical order
        # 
        # return self.rates
        # ------------------------------------------------


    def list_rates(self):
        """Return a list contaning all currencies in alphabetical order"""
        # Handle possible crasch if self.rates dict is empty by returning an empty list.
        if not self.rates: 
            return []

        # If dict contains data - return it sorted by alphabetical order. 
        # keys() used for getting only keys else we get key:values in dict stryle{}        
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
        app_id = "4ee8416577fd41128be96f5a18dbb9de"
        url = f"https://openexchangerates.org/api/latest.json?app_id={app_id}" # 4ee8416577fd41128be96f5a18dbb9de
        headers = {"accept": "application/json"}  # This needs to be added, it tells the API that they should return JSON
        

        try: 
            response = requests.get(url, headers=headers, timeout=10) # Send the request to the server, pass-in a timeout at 10 seconds or it will run indefinitely.

            if response.status_code == 200: # 200 status is OK!
                print("Success, data fetched from (server?)") # Give more information maby            

                data: dict[str, Any] = response.json() # Convert data to a .json, then into a dict and store it in variable "data".

                self.data = data # Self.data saves the "whole" JSON response.
                self.rates = data.get("rates", {}) # Looks for the value (every currency) from data - print a default value "{}" if "rates" does not exist.
                self.base = data.get("base", "USD") # Because USD is the only base we can work with. / .get requests the data from server (the base currency in this case)
                self.timestamp = data.get("timestamp") # Saves the last time data was timestamped (updated) / .get requests the data from server (the timestamp in this case)
                return data # Returns data for other instances(?) parts of the program to use.
            else:
                print("Non-sucess status code: ", response.status_code) # Give information about status-code (what went wrong).

        # Added a "catcher" for network errors (raises a ConnectionError exception).
        # Prevents program from crasching
        except requests.RequestException as e:
            print(f"Network error whilke fetching data: {e}")
            self.data = {}
            self.rates = {}
            self.timestamp = None
            return {}


    # RECOMMENT WHEN CODE STOPS BEING SO GOD DAMN CONFUSING.
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

        # Baisc number errorhandling
        if amount <= 0:
            raise ValueError("Error: amount must be greater than 0")

        # Create two variables to work with, uppsercase and strip them for better UI.
        convert_from = from_currency.upper().strip()
        convert_to = to_currency.upper().strip()

        # Basic errorhandling for currency code
        if convert_from not in self.rates or convert_to not in self.rates:
            raise ValueError ("Either currency converting from, or to are invalid.")

        # Create variable that takes self.rates dict to apply in coming conversion (to be able to do math)
        # What happens:
        # The convert from/to is the 3-letter code e.g. "SEK" / self.rates looks up the code in dict
        # The base is "USD", so now it knows 1USD = 10~SEK (which is stores in from_rate)
        # Same goes with to_rate e.g.: (1USD = 1EUR)
        from_rate = self.rates[convert_from]
        to_rate = self.rates[convert_to]

        # Convert the amount from the choosen rate to USD: 
        # Example: 100 SEK to USD (1USD ~= 10.5 SEK): 100 / 10.50 = 9.5~ (USD)
        base_amount = amount / from_rate
        # Convert the base amount (USD) to choosen rate e.g. EUR (1USD ~= 0.9EUR)
        # 0.95(USD(base_amount)) * 0.90(EUR(to_rate)) ~= 0.85(EUR(converted_amount))
        converted_amount = base_amount * to_rate

        # Return the evaluated result
        return converted_amount



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
        # If there's no data print msg and return.
        if not self.data:
            print("There's no data to export.")
            return
        

        # Open a file for writing ("w") "w" also creates file if it doesn't exist.
        # Create method parameter "filename" and use it below
        # .dump converts py dict to json string and writes it to the file.
        # indent=number gives a better structure to the exported file, else it will display as a long string with all info.
        try:
            with open(filename, "w") as file:
                json.dump(self.data, file, indent=4)

            print(f"Data successfully exported to: {filename}")

        except Exception as e:
            print(f"There was an error exporting data: {e}")


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

        # Create f-string and variables for app ID, URL and date.
        app_id = "4ee8416577fd41128be96f5a18dbb9de"
        url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={app_id}" # Change "date" to input

        try:
            # Create variable and get request for url, add connection timeout at 10 seconds.
            response = requests.get(url, timeout=10)
            # Checks for HTTP status code of the response and raises error if it's not correct.
            response.raise_for_status()
            # Create variable that stores the response as json (historical_data variable will be a dict format due to .json (converts it automatically))
            historical_data = response.json()
        
        # Basic error handling, return empty dict in this case (to avoid crash) - TRY TO BE MORE SPECIFIC HERE
        except Exception as e:
            print(f"Failed to fetch historical data: {e}") # TODO: How to implement the response.exceptions to catch all network issues? 
            return {}
        return historical_data


    # DONT KNOW IF THIS WORKS AS INTENDEND JUST YET, FIX MENUCHOICE AND THEN FIX DETAILS
    def list_historical_rates_for_currency(self, currency: str, days: str) -> list[tuple[str, str]]:
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

        results: list[tuple[str, str]] = [] # Store date and rate
        user_code = currency.strip().upper()

        # Sets the time to UTC
        # today = datetime.now(datetime.timezone.utc) # doesn't work -.- wtf

        # Sets time to UTC / .date() to remove time (only use date). Variable represents todays date in UTC.
        today = datetime.now(timezone.utc).date() # whaaaaaaaaaaaaaaaaaat?! lol you forgot to import timezone

        for i in range(days):
            prior_day = today - timedelta(days=i) # Math operation that goes back one day for each iteration.
            date_string = prior_day.strftime("%Y-%m-%d") # Returns a string representing date.

            new_data = self.get_historical_rate(date_string) # Reuse historical_rate method (date_string contains timestamp, rates).
            rate = new_data.get("rates", {}).get(user_code) # Get rates for target currency and store in rate variable, if not found - store in empty dict to avoid crash

            if rate:
                results.append((date_string, float(rate))) # If rate is found, add it to result and convert it to float (wrap in tuple so it takes two arguments).

        results.sort() # Sort the results.

        return results # Return the results.

