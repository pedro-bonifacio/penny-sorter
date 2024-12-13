import pandas as pd
import os

def selection_menu(options):
    print("\n------------- Detected files --------------")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:
        choice = int(input("\nEnter the number of the choice you want to select: "))
        if 1 <= choice <= len(options):
            selected_option = options[choice - 1]
            print(f"You selected: {selected_option}")
            return selected_option
        else:
            print(f"Invalid number.")

def import_clean_statement():
    input_files_path = './input_files_here/'

    banks = ['Montepio', 'Revolut']
    files = [f for f in os.listdir(input_files_path) if os.path.isfile(os.path.join(input_files_path, f))]

    selected_file = selection_menu(files)
    selected_bank = selection_menu(banks)

    selected_file_path = os.path.join(input_files_path, selected_file)

    if selected_bank == 'Montepio':
        statement = pd.read_csv(selected_file_path, encoding='ISO-8859-1', usecols=[1, 2, 3, 5])

        # Montepio
        statement.columns = ['date', 'description', 'value', 'balance']
        statement['date'] = pd.to_datetime(statement['date'], dayfirst=True)
        statement['value'] = statement['value'].str.replace(',', '.').astype(float)
        statement['balance'] = statement['balance'].str.replace(',', '.').astype(float)
        statement['description'] = statement['description'].str.rstrip()

    else:
        statement = pd.read_csv(selected_file_path, encoding='ISO-8859-1', usecols=[1, 2, 3, 5])

    return statement
