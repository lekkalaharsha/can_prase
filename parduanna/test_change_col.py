import pandas as pd

# Load the CSV files into DataFrames
volume_csv = 'result.csv'
fid_csv = 'Sevcon controller fault codes_Fault Codes.csv'
output_csv = 'output_file_chaged.csv'

# Read the volume CSV file
volume_df = pd.read_csv(volume_csv)

# Read the FID CSV file
fid_df = pd.read_csv(fid_csv, skiprows=3)

# Print column names for debugging
print("Volume CSV Columns:", volume_df.columns)
print("FID CSV Columns:", fid_df.columns)

# Ensure the 'FID' column in fid_df is treated as strings
fid_df['FID'] = fid_df['FID'].astype(str).str.strip()

# Add '0x' prefix to the 'Hex Code' column values
volume_df['Hex Code'] = volume_df['Hex Code'].apply(lambda x: f'0x{x}')

# Merge the DataFrames on the hex code and FID value
merged_df = pd.merge(volume_df, fid_df, left_on='Hex Code', right_on='FID', how='left')

# Select and reorder the columns as specified
output_columns = [
    'Time',
    'controller_fault_status_1_REAR.motorcontroller_1 fault_code',
    'Hex Code',
    'FID',
    'Message',
    'Description',
    'Type',
    'Display',
    'Recommended Action'
]

# Create the final DataFrame with the selected columns
final_df = merged_df[output_columns]

# Save the resulting DataFrame to a new CSV file
final_df.to_csv(output_csv, index=False)

print(f"Resulting data saved to {output_csv}")