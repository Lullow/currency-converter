from typing import Any

import requests

from currencyhandler import CurrencyHandler

# DO NOT UPLOAD A VIRTUAL ENVIRONMENT TO GIT
# Add the name of your virtual environment to .gitignore
# Now you can git add and git commit.
# Remove the pass keyword from the method when you start implementing the method

# REMEMBER TO MAKE COMMITS FREQUENTLY! I don't want to see only 1 commit with all the code in it.
# You can remove these comments^

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
        print("[0] - List all currencies")
        print("[1] - Convert USD to a currency of choice")
        print("[2] - Refresh the data (fetch new currency data)")
        print("[3] - Export the data to JSON")
        print("[4] - Convert from any currency to any currency")
        print("[5] - Get historical exchange rate")
        print("[6] - Get rate trend for a currency")
        print("[7] - Exit the application")

        choice = input("Enter your choice (0-7): ")

        # USE BASIC CLEAN CODE IN IF/ELIF-STATEMENTS!
        # DO ONE CHOICE AT TIME IF POSSIBLE
        # BREAK DOWN THE BIG PROBLEM TO SMALLER PROBLEMS.
        # TRY / EXCEPT IN ALL USERCHOICES?

        # Baisc errorhandling at the moment, maby improve?
        if choice == "0":
            try:
                listing_currencies = currency_handler.list_rates()

                if not listing_currencies:
                    print("No data avaliable, try refreshing data: [Menu option: 2].")
                else:
                    print(", ".join(listing_currencies)) # ", ".join added for better terminal feedback.

            except Exception as e:
                print(f"Error when listing currencies: {e}")


        elif choice == "1":
            convert_to = input("Convert USD to currency (e.g. EUR): ").strip().upper() # Use upper here to print out more userfriendy response later.
            raw_user_amount = input("Enter amount in USD: ").strip() 

            try:
                user_amount = float(raw_user_amount) # Convert to float and store in new variable.
                result = currency_handler.convert_from_usd(convert_to, user_amount) # Class method to do math -> store in variable
                print(f"Amount: {user_amount:.2f} USD = {result:.2f} {convert_to}") # Print out result in formatted 2 decimal amount.

            # Catch negative numbers/strings
            except ValueError as e:                
                print(f"Conversion error: {e}")
            # Catch unexpected errors
            except Exception as e:                
                print(f"Unexpected error ocurred: {e}")

        # Calls fetch method again to update rates.
        elif choice == "2":
            try:
                currency_handler.fetch_currency_data()
                print("Refreshed")
            # Catch unexpected errors
            except Exception as e:
                print(f"Refresh failed: {e}")

        # TODO: FIX TIMESTAMP - Right now it shows: "timestamp": 1760878814 - HOW?
        # Possible try/except block here?
        # Use currency_handler variable to import export method. 
        elif choice == "3":
            currency_handler.export_to_json("updated_rates.json")

        elif choice == "4":
            user_from = input("What currency do you want to convert FROM? - (e.g. SEK): ").strip().upper() # strip and upper methods for friendlier UI experience.
            user_to = input("What currency do you want to convert TO? - (e.g. SEK): ").strip().upper()
            user_amount = input("What amount: ").strip()

            try:
                user_amount_float = float(user_amount) # Convert to float
                result = currency_handler.convert_any_currency(user_from, user_to, user_amount_float) # Use convert any currency method to do the conversion.
                print(f"You converted {user_amount_float:.2f} {user_from} to {user_to}.") 
                print(f"Final payout: {result:.2f} {user_to}.")

            # Catch input that's not numbers, negative or wrong currency code. Also unexcepcted errors, and handle them without crasching the program.
            except ValueError as e:
                print(f"There was an error when converting currency: {e}")
            except Exception as e:
                print(f"Unexpected error ocurred: {e}")

        elif choice == "5":
            date = input("Enter date to check (YYYY-MM-DD): ").strip()

            try:
                historical_date_data = currency_handler.get_historical_rate(date)

                if not historical_date_data:
                    print("Historical data was not found.")
                else:
                    # .get() reads the value of the key 'timestamp' / 'base' and prints it. 
                    print(f"Timestamp: {historical_date_data.get('timestamp')}")
                    print(f"Base: {historical_date_data.get('base')}")

                    # code represents the 3-letter code, rate represents the value, items() iterates key, value pairs.
                    for code, rate in list(historical_date_data.items()):
                        print(f"{code}: {rate}") # The terminal get's cluttery with this approach, how to fix?

            except Exception as e:
                print(f"Error fetching historical rates: {e}")

        elif choice == "6":
            pass # fetch error?

        elif choice == "7":
            print("Thank you for using th e Currency Converter. Goodbye!")
            break # can this fail? 

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


# UPDATE STEP 2:

# main.py: choice:0 : ", ".join added for better terminal feedback.
# cyrrency.py: fetch module: Added a "catcher" for network errors (raises a ConnectionError exception).
# moved up my variables in fetch currency inside if-statement. Else it would still print currencylist even though error might occur.
#
# Start wokring with convert from usd method:
# Do error handling - valueerrors for negative numbers and currencies that doesn't exist.
# Convert currency 3 letter "code" to uppercase & strip it.
# Apply math from to currency parameter (usd) to rate (the currency user want to convert) and return the product in float type.


# choice1: 
# Ask user for currency to convert -> ask for amount -> strip it and uppercase it to use later in print.
# Convert to float.
# Fetch method that does math and store in new variable.
# Print formatted result.
# Catch basic errors with try/except - print them.


# choice2:
# Call method to refresh rates by importing them again.
# Catch baisc errors with try/except - print them.


# --------------
# SIDE NOTES: ON THE GO NOTES:
# Do I need to import os / json to handle exports / loading files?
# os can store API key in a variable (so it's not hardcoded).
# self.data IS WHERE INFORMATION ABOUT CURRENCYS ARE STORED!
# TIMESTAMP INFO? (see update 3 on current time formatted - isoformat()) - FIX WHEN REST OF CLASSMETHODS ARE IMPLEMENTED!
# --------------


# UPDATE STEP 3: (EXPORT DATA TO JSON)

# https://realpython.com/read-write-files-python/ - File handling (open, write, read) 

# https://docs.python.org/3/library/os.html#os.makedirs - import os for using os.makedirs(), os.path.exists(), os.path.dirname().

# https://www.w3schools.com/python/python_datetime.asp - current time formatted - isoformat()

# Start building very basic code to convert json-formatted string - DONE
# Handle potential (baisc) errors - DONE
# HOW TO INCLUDE THE CURRENT TIMESTAMP ? ? ? ? ? ? ?


# UPDATE STEP 4: (Convert from any currency to any currency)
# Where to begin?
# From currency -> to currency (use the 3 letter "code")
# Handle amount math
# Return the "to currency"
# Catch errors - invalid currency / invalid amount (0 or negative)


# UPDATE STEP 5: Get historical exchange rate
# Goal - fetch last exchange rates (from a specific date)
# So basically user want to see what SEK was worth 2025-01-01
# Access API historical data -> Get json
# NOW TO FIX THE TIMESTAMP AT STEP 3 ALSO - NEED TO GET YYYY-MM-DD format!!
# Can I use list_rate method to do this, or do I need to apply code in historical method? Do own code in new method.
# Do I need to add more parameters to method?
# Do I need to import date time? Yes. Better date format for menuchoice 3 and this one.


# Start by placing app_id and url (same as list_rate)
# Do a .get request, timeout included
# handle errors with try except - check how you did list_rates
# return as dict (store it in dict or list)

# Menu choice:
# Use 3 letter code for getting data
# apply try/except (check if date is avaliable / format input correct / other errors)

# OBS! each day requested counts as one API request 
# (so requesting a full month of data will count as up to 31 ‘hits’"
# Where the requested end date is not a valid calendar date, 
# it will be corrected backwards automatically to the nearest valid day