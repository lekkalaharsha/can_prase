import pandas as pd

# Load the CSV files into DataFrames
volume_csv = 'result.csv'  # Replace with your Volume Name CSV file name
fid_csv = 'Sevcon controller fault codes_Fault Codes.csv'  # Replace with your FID CSV file name
output_csv = 'output_file.csv'  # Replace with your desired output file name

# Read the volume CSV file
volume_df = pd.read_csv(volume_csv)

# Read the FID CSV file
fid_df = pd.read_csv(fid_csv,skiprows=3)

# Print column names for debugging
print("Volume CSV Columns:", volume_df.columns)
print("FID CSV Columns:", fid_df.columns)

# Ensure the 'Volume Name' column in volume_df is treated as strings


# Ensure the 'FID' column in fid_df is treated as strings
fid_df['FID'] = fid_df['FID'].astype(str).str.strip()

# Add '0x' prefix to the 'Volume Name' column values
volume_df['Hex Code'] = volume_df['Hex Code'].apply(lambda x: f'0x{x}')

# Merge the DataFrames on the hex code and FID value
merged_df = pd.merge(volume_df, fid_df, left_on='Hex Code', right_on='FID', how='left')

# Save the resulting DataFrame to a new CSV file
merged_df.to_csv(output_csv, index=False)

print(f"Resulting data saved to {output_csv}")
