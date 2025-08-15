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

        if choice == "0":
            pass

        elif choice == "1":
            pass

        elif choice == "2":
            pass

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == "5":
            pass

        elif choice == "6":
            pass

        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
