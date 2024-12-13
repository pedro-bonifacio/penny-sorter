import pandas as pd
from categories import expense_categories, expenses_subcategories, income_categories, income_subcategories
import sys
sys.path.append('./secrets/')
from recurrent import recurrent


def category_menu(transaction):
    if transaction['description'].startswith("LEV.ATM"):
        return "Miscellaneous", "ATM Withdrawals"

    if transaction['is_income']:
        categories = income_categories
        subcategories = income_subcategories
    else:
        categories = expense_categories
        subcategories = expenses_subcategories

    while True:  # Loop for category selection
        print("\n------------- Available Categories --------------")
        for index, cat in enumerate(categories, start=1):
            print(f"{index}. {cat}")

        print(f"\nDescription: '{transaction['description']}'")
        print("Date: {}".format(str(transaction['date']).split(" ")[0]))
        print(f"Value: {transaction['value']}€")

        try:
            choice = int(input("\nEnter the number of the choice you want to select: "))
            if 1 <= choice <= len(categories):
                selected_cat = categories[choice - 1]
                print(f"You selected: {selected_cat}")

                while True:  # Loop for subcategory selection
                    print("\n------------- Available Sub-Categories --------------")
                    for i, sub in enumerate(subcategories[selected_cat], start=1):
                        print(f"{i}. {sub}")
                    print("0. Go Back")

                    print(f"\nDescription: '{transaction['description']}'")
                    print("Date: {}".format(str(transaction['date']).split(" ")[0]))
                    print(f"Value: {transaction['value']}€")

                    sub_choice = int(input("\nEnter the number of the choice you want to select (0 to go back): "))
                    if sub_choice == 0:
                        print("Going back to category selection...\n")
                        break  # Go back to category selection
                    elif 1 <= sub_choice <= len(subcategories[selected_cat]):
                        selected_sub = subcategories[selected_cat][sub_choice - 1]
                        print(f"You selected category '{selected_cat}' and sub-category '{selected_sub}'")
                        return selected_cat, selected_sub  # Exit both loops
                    else:
                        print("Invalid number. Please try again.")
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def categorize_transactions(statement):
    # Create an empty Series to hold the categories
    statement['is_income'] = statement['value'] > 0
    categories_series = pd.Series(index=statement.index, dtype="object")
    subcategories_series = pd.Series(index=statement.index, dtype="object")

    for index, transaction in statement.iterrows():
        description = transaction['description']

        if description in recurrent:
            categories_series.at[index], subcategories_series.at[index] = recurrent[description]
        else:
            category, subcategory = category_menu(transaction)
            categories_series.at[index] = category
            subcategories_series.at[index] = subcategory

    # Append the new categories as a column to the DataFrame
    statement['category'] = categories_series
    statement['subcategory'] = subcategories_series

    return statement
