from penny_cleaner import import_clean_statement
from penny_mapper import categorize_transactions


raw_statement = import_clean_statement()
statement = categorize_transactions(raw_statement)