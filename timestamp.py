import re
import datetime
import cantools
import csv

# Define the path to your DBC file
dbc_file_path = 'Zekrom_CANbus_1.dbc'

# Load the DBC file
db = cantools.database.load_file(dbc_file_path)

# Regular expression pattern for parsing CAN log lines
log_pattern = re.compile(r'\((\d+\.\d+)\) (\S+) (\S+)#(\S*)')

def parse_can_message(line, specified_can_id):
    """Parse a single CAN message line and return the decoded data."""
    match = log_pattern.match(line)
    if not match:
        return None

    timestamp_str, interface, can_id, data = match.groups()

    # Check if the extracted CAN ID matches the specified CAN ID
    if can_id != specified_can_id:
        return None

    timestamp = float(timestamp_str)
    # Convert the timestamp to a human-readable format with date and time
    human_readable_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    # Convert data bytes to a byte array
    data_bytes = bytes.fromhex(data)

    # Decode the CAN message using the DBC file
    try:
        can_id_int = int(can_id, 16)
        message_obj = db.get_message_by_frame_id(can_id_int)
        decoded_data = message_obj.decode(data_bytes) if message_obj else {}
    except KeyError:
        print(f"CAN ID {can_id} not found in the DBC file.")
        decoded_data = {}

    return {
        "timestamp": human_readable_timestamp,
        "interface": interface,
        "can_id": can_id,
        "data_bytes": data,
        **decoded_data  # Add decoded data to the result
    }

def process_log_file(log_file_path, specified_can_id, csv_file_path):
    """Process the log file and write the decoded data to a CSV file."""
    # List to store parsed messages
    parsed_messages = []
    signal_names = []

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.strip():
                parsed_message = parse_can_message(line, specified_can_id)
                if parsed_message:
                    parsed_messages.append(parsed_message)
                    # Add new signal names to the list in the order they appear
                    for key in parsed_message.keys():
                        if key not in signal_names and key not in ['timestamp', 'interface', 'can_id', 'data_bytes']:
                            signal_names.append(key)

    # Define the CSV header
    header = ['timestamp', 'interface', 'can_id', 'data_bytes'] + signal_names

    # Sort messages by timestamp
    parsed_messages.sort(key=lambda x: datetime.datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S'))

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        # Write each sorted message to the CSV
        for message in parsed_messages:
            # Ensure all keys are present in the row, fill missing signals with empty values
            row = {key: message.get(key, '') for key in header}
            writer.writerow(row)

    print(f'CSV file "{csv_file_path}" with CAN ID {specified_can_id} has been created successfully.')

# Specify the CAN ID to filter
specified_can_id = input("Enter the CAN ID: ")


process_log_file('candump-2024-07-18_013952.log.1', specified_can_id, 'timestamp_1.csv')
