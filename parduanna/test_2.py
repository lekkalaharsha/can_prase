import pandas as pd

# Load the CSV files into DataFrames
volume_csv = 'volume_file.csv'  # Replace with your Volume Name CSV file name
fid_csv = 'Sevcon controller fault codes_Fault Codes.csv'  # Replace with your FID CSV file name
output_csv = 'output_file.csv'  # Replace with your desired output file name

# Read the volume CSV file
volume_df = pd.read_csv(volume_csv)

# Read the FID CSV file
fid_df = pd.read_csv(fid_csv)

# Print column names for debugging
print("Volume CSV Columns:", volume_df.columns)
print("FID CSV Columns:", fid_df.columns)

# Ensure the 'Volume Name' column in volume_df is treated as strings
volume_df['Volume Name'] = volume_df['Volume Name'].astype(str).str.strip()

# Ensure the 'FID' column in fid_df is treated as strings
fid_df['FID'] = fid_df['FID'].astype(str).str.strip()

# Add '0x' prefix to the 'Volume Name' column values
volume_df['Volume Name Hex'] = volume_df['Volume Name'].apply(lambda x: f'0x{x}')

# Remove '0x' prefix from the 'FID' column values for comparison
fid_df['FID Clean'] = fid_df['FID'].apply(lambda x: x[2:] if x.startswith('0x') else x)

# Remove '0x' prefix from 'Volume Name Hex' for comparison
volume_df['Volume Name Clean'] = volume_df['Volume Name Hex'].apply(lambda x: x[2:])

# Merge the DataFrames on the cleaned hex code and FID value
merged_df = pd.merge(volume_df, fid_df, left_on='Volume Name Clean', right_on='FID Clean', how='left')

# Drop intermediate columns used for merging
merged_df.drop(columns=['Volume Name Hex', 'Volume Name Clean', 'FID Clean'], inplace=True)

# Save the resulting DataFrame to a new CSV file
merged_df.to_csv(output_csv, index=False)

print(f"Resulting data saved to {output_csv}")
