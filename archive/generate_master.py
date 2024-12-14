import os
import pandas as pd

# Define the folder containing the CSV files
input_folder = "monthly_statements"
output_file = "master_statement.csv"

# Check if the folder exists
if not os.path.exists(input_folder):
    raise FileNotFoundError(f"The folder '{input_folder}' does not exist!")

# Initialize an empty list to store DataFrames
data_frames = []

# Iterate through all CSV files in the folder
for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(input_folder, file)
        try:
            # Read each CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the required columns exist
            required_columns = ["date", "description", "value", "balance", "is_income", "category", "subcategory"]
            if not all(col in df.columns for col in required_columns):
                print(f"Skipping file '{file}' as it does not contain the required columns.")
                continue

            data_frames.append(df)
            print(f"Successfully read file: {file}")
        except Exception as e:
            print(f"Error reading file '{file}': {e}")

# Combine all DataFrames into a single DataFrame
if not data_frames:
    print("No valid CSV files found. Exiting.")
else:
    combined_df = pd.concat(data_frames, ignore_index=True)

    # Remove duplicate rows
    combined_df = combined_df.drop_duplicates()

    # Ensure 'date' column is in datetime format
    combined_df["date"] = pd.to_datetime(combined_df["date"], errors='coerce')

    # Drop rows with invalid 'date' values (NaT)
    combined_df = combined_df.dropna(subset=["date"])

    # Sort the DataFrame by the 'date' column
    combined_df = combined_df.sort_values(by="date")

    # Export the cleaned and combined data to a new CSV file
    combined_df.to_csv(output_file, index=False)

    print(f"Combined CSV file has been created: {output_file}")
