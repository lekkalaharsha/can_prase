import pandas as pd

# Define file names
volume_csv = 'result.csv'  # Replace with your Volume Name CSV file name
fid_csv = 'Sevcon controller fault codes_Fault Codes.csv'  # Replace with your FID CSV file name
output_csv = 'output_file_2.csv'  # Replace with your desired output file name

try:
    # Read the volume CSV file
    volume_df = pd.read_csv(volume_csv)

    # Read the FID CSV file
    fid_df = pd.read_csv(fid_csv,skiprows=3)
    
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

# Print column names for debugging
print("Volume CSV Columns:", volume_df.columns)
print("FID CSV Columns:", fid_df.columns)

# Ensure the 'Volume Name' column in volume_df is treated as strings
volume_df['Hex Code'] = volume_df['Hex Code'].astype(str).str.strip()

# Ensure the 'FID' column in fid_df is treated as strings
fid_df['FID'] = fid_df['FID'].astype(str).str.strip()

# Add '0x' prefix to the 'Volume Name' column values
volume_df['Hex Code'] = volume_df['Hex Code'].apply(lambda x: f'0x{x}')

# Remove '0x' prefix from the 'FID' column values for comparison
fid_df['FID'] = fid_df['FID'].apply(lambda x: x[2:] if x.startswith('0x') else x)

# Remove '0x' prefix from 'Volume Name Hex' for comparison
volume_df['Hex Code'] = volume_df['Hex Code'].apply(lambda x: x[2:])

# Merge the DataFrames on the cleaned hex code and FID value
merged_df = pd.merge(volume_df, fid_df, left_on='Hex Code', right_on='FID', how='left')

# Drop intermediate columns used for merging
# merged_df.drop(columns=['Hex Code', 'Hex Code', 'FID'], inplace=True)

# Save the resulting DataFrame to a new CSV file
merged_df.to_csv(output_csv, index=False)

print(f"Resulting data saved to {output_csv}")
