import pandas as pd

# Load the CSV files into DataFrames
output_csv = 'result.csv'  # Replace with your input file name
input_csv = 'Sevcon controller fault codes_Fault Codes.csv'  # Replace with your desired output file name
df = pd.read_csv(input_csv, skiprows=3)
# Read the input CSV file



# Get user input (assuming input is a hexadecimal string like '0x4411')
user_input_hex = input("Enter the fid value (in hexadecimal, e.g., 0x4411): ")


column_name = 'FID'  # Replace with the correct column name

# Filter rows based on the user input
if column_name in df.columns:
    filtered_df = df[df[column_name] == user_input_hex]
    # Save the filtered rows to a new CSV file
    filtered_df.to_csv(output_csv, index=False)
    print(f"Filtered data saved to {output_csv}")
else:
    print(f"Column '{column_name}' does not exist in the CSV file.")