import csv
import datetime

# Define the path to your log file
log_file_path = 'candump-2024-07-22_091800.log.1'

# Function to parse a single CAN message line
def parse_can_message(line):
    try:
        # Remove the newline character and any leading/trailing spaces
        line = line.strip()

        # Split timestamp and the rest of the message
        timestamp_str, message = line.split(') ')
        timestamp = float(timestamp_str.strip('('))

        # Split interface and CAN ID/data
        interface, can_data = message.split(' ')

        # Split CAN ID and data
        can_id, data = can_data.split('#')

        # Convert timestamp to a human-readable format
        human_readable_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

        # Split the data into bytes, handle empty data case
        data_bytes = [data[i:i + 2] for i in range(0, len(data), 2)] if data else []

        # Convert data bytes to integers for further processing
        data_integers = [int(byte, 16) for byte in data_bytes if byte]

        return {
            "timestamp": human_readable_timestamp,
            "interface": interface,
            "can_id": can_id,
            "data_bytes": data_bytes,
            
        }
    except Exception as e:
        print(f"Error parsing line: {line.strip()} - {e}")
        return None

# Read the log file with error handling
try:
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"Log file '{log_file_path}' not found.")
    exit(1)
except IOError as e:
    print(f"Error reading log file '{log_file_path}': {e}")
    exit(1)

# Parse all messages
parsed_messages = [parse_can_message(line) for line in lines if line.strip()]

# Filter out any None values from parsing errors
parsed_messages = [msg for msg in parsed_messages if msg]

# Specify the CAN ID to filter
specified_can_id = input("Enter the CAN ID: ")

# Filter messages by the specified CAN ID
filtered_messages = [msg for msg in parsed_messages if msg['can_id'] == specified_can_id]

# Define the CSV file path for filtered messages
csv_file_path = 'filtered_can_messages.csv'

# Define the CSV header
csv_header = ['timestamp', 'interface', 'can_id', 'data_bytes']

# Write the filtered messages to the CSV file with error handling
try:
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        
        # Write the header
        writer.writeheader()
        
        # Write each filtered message
        for message in filtered_messages:
            # Convert data_bytes to strings for CSV storage
            message['data_bytes'] = ' '.join(message['data_bytes'])
            
            # Write the row
            writer.writerow(message)
except IOError as e:
    print(f"Error writing CSV file '{csv_file_path}': {e}")
    exit(1)

print(f'CSV file "{csv_file_path}" with CAN ID {specified_can_id} has been created successfully.')
