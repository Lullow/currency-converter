from typing import Any

import requests

from currencyhandler import CurrencyHandler

# Think of the CurrencyHandler as a class that should strictly only handle functionality.
# Using print, input or similar should be done outside of the class, in such way
# that you COULD use the currencyhandler in any type of application that might
# want to use currencies


def main() -> None:
    """
    The main function that runs the currency conversion application.

    This function should:
    1. Create an instance of the CurrencyHandler class.
    2. Display a menu of options to the user.
    3. Handle user input and call the appropriate methods of the CurrencyHandler.
    4. Provide a loop to allow multiple operations in a single session.
    5. Handle any errors or exceptions that may occur during operation.

    Menu options should include:
    [0] - List all currencies
    [1] - Convert USD to a currency of choice
    [2] - Manually refresh the data (fetch new currency data)
    [3] - Export the data to JSON
    [4] - Convert from any currency to any currency
    [5] - Get historical exchange rate
    [6] - List historical rates for a currency + more
    [7] - Exit the application
    """
    # Use this instance of CurrencyHandler to do stuff in your menu.
    currency_handler = CurrencyHandler()


    while True:
        print("\nCurrency Converter Menu:")
        print("[0] - List all currencies in alphabetical order")
        print("[1] - Convert USD to a currency of choice")
        print("[2] - Refresh the data (fetch new currency data)")
        print("[3] - Export the data to JSON")
        print("[4] - Convert from any currency to any currency")
        print("[5] - Get historical exchange rate")
        print("[6] - Get rate trend for a currency")
        print("[7] - Exit the application")

        choice = input("Enter your choice (0-7): ")


        if choice == "0":
            try:
                listing_currencies = currency_handler.list_rates()

                if not listing_currencies:
                    print("No data avaliable, try refreshing data: [Menu option: 2].")
                else:
                    # ", ".join added for better terminal feedback.
                    print(", ".join(listing_currencies))

            except Exception as e:
                print(f"Error when listing currencies: {e}")

        elif choice == "1":
            # Use upper here to print out more userfriendy response later.
            convert_to = input("Convert USD to currency (e.g. EUR): ").strip().upper()
            raw_user_amount = input("Enter amount in USD: ").strip() 

            try:
                # Convert to float and store in new variable.
                user_amount = float(raw_user_amount)
                # Class method to do math -> store in variable.
                result = currency_handler.convert_from_usd(convert_to, user_amount)
                # Print out result in formatted 2 decimal amount.
                print(f"Amount: {user_amount:.2f} USD = {result:.2f} {convert_to}")

            # Catch negative numbers/strings
            except ValueError as e:                
                print(f"Conversion error: {e}")
            # Catch unexpected errors
            except Exception as e:                
                print(f"Unexpected error ocurred: {e}")
        
        elif choice == "2":
            try:
                currency_handler.fetch_currency_data()
                print("Refreshed")
            # Catch unexpected errors
            except Exception as e:
                print(f"Refresh failed: {e}")

        elif choice == "3":
            try:
                currency_handler.export_to_json()
                print("Data exported successfully.")
            except ValueError as e:
                print(f"{e}")
            except IOError as e:
                print(f"Could not write file: {e}")

        elif choice == "4":
            # strip and upper methods for friendlier UI experience.
            user_from = input("What currency do you want to convert FROM? - (e.g. SEK): ").strip().upper()
            user_to = input("What currency do you want to convert TO? - (e.g. SEK): ").strip().upper()
            user_amount = input("What amount: ").strip()

            try:
                # Convert to float.
                user_amount_float = float(user_amount)
                # Use convert any currency method to do the conversion.
                result = currency_handler.convert_any_currency(user_from, user_to, user_amount_float)
                print(f"You converted {user_amount_float:.2f} {user_from} to {result:.2f} {user_to}.") 
                print(f"Final payout: {result:.2f} {user_to}.")

            # Catch input that's not numbers, negative or wrong currency code. Also unexcepcted errors, and handle them without crasching the program.
            except ValueError as e:
                print(f"There was an error when converting currency: {e}")
            except Exception as e:
                print(f"Unexpected error ocurred: {e}")

        elif choice == "5":
            date = input("Enter date to check (YYYY-MM-DD): ").strip()
            print("This gets the historical data from todays date, going back to the date chosen.")

            try:
                historical_date_data = currency_handler.get_historical_rate(date)

                if not historical_date_data:
                    print("Historical data was not found.")
                else:
                    # .get() reads the value of the key 'timestamp' / 'base' and prints it. 
                    print(f"Timestamp: {historical_date_data.get('timestamp')}")
                    print(f"Base: {historical_date_data.get('base')}")

                    # code represents the 3-letter code, rate represents the value, items() iterates key, value pairs.
                    # print out the 10 first currencies (which will be in alphabetical order..) Good idé?
                    for code, rate in list(historical_date_data.get('rates', {}).items())[:10]:
                        print(f"{code}: {rate}")

            except Exception as e:
                print(f"Error fetching historical rates: {e}")

        elif choice == "6":
            user_code = input("Enter currency code: (e.g.: SEK): ").strip().upper()
            user_days_str = input("Enter how many days back from current date you want to lookup: ").strip()

            # Convert user input to int.
            # Fetch class method, convert userinput for day lookup to int - store in variable.
            user_days = int(user_days_str)
            date_rate_list = currency_handler.list_historical_rates_for_currency(user_code, user_days)

            try: 
                if not date_rate_list:
                    print("No historical data found.")
                else:
                    print(f"{user_code} vs USD for the last {user_days} days: {date_rate_list}")
            except ValueError:
                # Catch valueerrors from input.
                print("Please enter digits when looking up prior dates.")
            except Exception as e:
                # Catch unexpected errors to aviod crash.
                print(f"Unknown error while handling historical data: {e}")

        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


# elif2:"<bound method Response.raise_for_status of <Response [200]>>" Can I fix? - printed out the the method instead of calling it - FIXED.

# elif3: Right now the timestamp outputs this: ""timestamp": 1761465617," Can I fix? 

# elif5: Error fetching historical rates: 'dict_items' object is not subscriptable - missplaced parantheses - FIXED.

# # .get is not getting the same yellow highlight as it's supposed to - but it works.. (line 326 in currencyhandler.py) I don't know how to fix it.



# API key not hardcoded - fix?

# Don't know if it's a good idé to show 10x of rates when choosing "get historical exchange rate" or to show all the currencies.

