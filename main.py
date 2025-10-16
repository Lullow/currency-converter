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

        # Calls fetch method again to get rates again.
        elif choice == "2":
            try:
                currency_handler.fetch_currency_data()
                print("Refreshed")
            # Catch unexpected errors
            except Exception as e:
                print(f"Refresh failed: {e}")

        elif choice == "3":
            pass # export failed?

        elif choice == "4":
            pass # couldnt convert currency?

        elif choice == "5":
            pass # ?

        elif choice == "6":
            pass # fetch error?

        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
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
# 
# choice1: 
# Ask user for currency to convert -> ask for amount -> strip it and uppercase it to use later in print.
# Convert to float.
# Fetch method that does math and store in new variable.
# Print formatted result.
# Catch basic errors with try/except - print them.
#
#
# choice2:
# Call method to refresh rates by importing them again.
# Catch baisc errors with try/except - print them.



# SIDE NOTES: ON THE GO NOTES:
# Do I need to import os / json to handle exports / loading files?
# os can store API key in a variable (so it's not hardcoded).
# 