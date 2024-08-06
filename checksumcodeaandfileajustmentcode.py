#AUTHOR : LEKKALA HARSHA VARDHAN NAIDU
#DATE: 26-07-2024

import pandas as pd
from datetime import datetime

# Load the CSV files into DataFrames
volume_csv = 'result.csv'
fid_csv = 'Sevcon controller fault codes_Fault Codes.csv'
output_csv = 'moteridchecksum.csv'

# Read the volume CSV file
volume_df = pd.read_csv(volume_csv)

# Read the FID CSV file
fid_df = pd.read_csv(fid_csv, skiprows=3)

# Print column names for debugging
print("Volume CSV Columns:", volume_df.columns)
print("FID CSV Columns:", fid_df.columns)

# Ensure the 'FID' column in fid_df is treated as strings
fid_df['FID'] = fid_df['FID'].astype(str).str.strip()

# Function to determine BMS checksum
def get_bms_checksum(date):
    if date > datetime(2023, 11, 14):
        return 'A1ED'
    elif date > datetime(2023, 7, 5):
        return '9F10'
    elif date > datetime(2023, 5, 27):
        return '96AC'
    return ''

# Function to determine Motor Nodes checksums
def get_motor_checksums(date):
    if date > datetime(2023, 7, 4):
        return '4FDC', 'CBF1'
    elif date > datetime(2023, 6, 26):
        return 'EE2F', '9727'
    elif date > datetime(2023, 6, 19):
        return 'EE2F', '9727'
    return '', ''

# Add '0x' prefix to the 'Hex Code' column values
volume_df['Hex Code'] = volume_df['Hex Code'].apply(lambda x: f'0x{x}')

# Convert 'Time' column to datetime
volume_df['Time'] = pd.to_datetime(volume_df['Time'])

# Extract date, month, year, and time from the 'Time' column
volume_df['Date'] = volume_df['Time'].dt.day
volume_df['BMS_Checksum'] = volume_df['Time'].apply(get_bms_checksum)
volume_df['Month'] = volume_df['Time'].dt.month
volume_df['Year'] = volume_df['Time'].dt.year
volume_df['Time_Only'] = volume_df['Time'].dt.time

# Apply motor checksums
motor_checksums = volume_df['Time'].apply(get_motor_checksums)
volume_df['MOTOR_NODE_1_CHECKSUM'], volume_df['MOTOR_NODE_2_CHECKSUM'] = zip(*motor_checksums)

# Merge the DataFrames on the hex code and FID value
merged_df = pd.merge(volume_df, fid_df, left_on='Hex Code', right_on='FID', how='left')

# Add a serial number column
merged_df['Serial_Number'] = range(1, len(merged_df) + 1)

# Select and reorder the columns as specified
output_columns = [
    'Serial_Number',
    'Date',
    'Month',
    'Year',
    'Time_Only',
    'controller_fault_status_1_REAR.motorcontroller_1 fault_code',  # Ensure this column exists
    'Hex Code',  # Replace 'Hex Code' with actual column name
    'FID',
    'Message',
    'Description',
    'Type',
    'Display',
    'BMS_Checksum',
    'MOTOR_NODE_1_CHECKSUM',
    'MOTOR_NODE_2_CHECKSUM',
    'Recommended Action'
]

# Check if all the specified columns exist in merged_df

# Create the final DataFrame with the selected columns
final_df = merged_df[output_columns]

# Save the resulting DataFrame to a new CSV file
final_df.to_csv(output_csv, index=False)

print(f"Resulting data saved to {output_csv}")
