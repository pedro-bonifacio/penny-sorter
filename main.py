from penny_cleaner import import_clean_statement
from penny_mapper import categorize_transactions


if __name__ == '__main__':
    raw_statement = import_clean_statement()
    statement = categorize_transactions(raw_statement)
    year_month = str(statement['date'].iloc[3].year) + '-' + str(statement['date'].iloc[3].month)
    statement.to_csv(f'./archive/monthly_statements/{year_month}.csv', index=False)