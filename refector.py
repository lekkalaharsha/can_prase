import re
import datetime
import cantools
import csv

# Define the path to your DBC file
dbc_file_path = 'Zekrom_CANbus_1.dbc'

# Load the DBC file
db = cantools.database.load_file(dbc_file_path)

# Regular expression pattern for parsing CAN log lines
log_pattern = re.compile(r'\((\d+\.\d+)\) (\S+) (\S+)#(\S+)')

def parse_can_message(line, specified_can_id):
    # Extract the CAN ID and check if it matches the specified CAN ID
    match = log_pattern.match(line)
    if not match:
        return None

    timestamp_str, interface, can_id, data = match.groups()

    # Check if the extracted CAN ID matches the specified CAN ID
    if can_id != specified_can_id:
        return None

    timestamp = float(timestamp_str)

    # Convert timestamp to a human-readable format
    human_readable_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

    # Convert data bytes to a byte array
    data_bytes = bytes.fromhex(data)

    # Decode the CAN message using the DBC file
    try:
        # Convert CAN ID from hex to int
        can_id_int = int(can_id, 16)
        message_obj = db.get_message_by_frame_id(can_id_int)
        decoded_data = message_obj.decode(data_bytes) if message_obj else None
    except KeyError:
        print(f"CAN ID {can_id} not found in the DBC file.")
        decoded_data = None

    return {
        "timestamp": human_readable_timestamp,
        "interface": interface,
        "can_id": can_id,
        "data_bytes": data,
        "decoded_data": decoded_data
    }

def process_log_file(log_file_path, specified_can_id, csv_file_path):
    with open(log_file_path, 'r') as log_file, open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['timestamp', 'interface', 'can_id', 'data_bytes', 'decoded_data'])
        writer.writeheader()
        
        batch_size = 1000
        batch = []

        for line in log_file:
            if line.strip():
                parsed_message = parse_can_message(line, specified_can_id)
                if parsed_message:
                    # Convert decoded_data to a string for CSV storage
                    parsed_message['decoded_data'] = str(parsed_message['decoded_data'])
                    batch.append(parsed_message)
                    
                    # Write the batch to CSV when it reaches the batch size
                    if len(batch) >= batch_size:
                        writer.writerows(batch)
                        batch = []

        # Write any remaining messages in the batch
        if batch:
            writer.writerows(batch)

    print(f'CSV file "{csv_file_path}" with CAN ID {specified_can_id} has been created successfully.')

# Specify the CAN ID to filter
specified_can_id = input("Enter the CAN ID: ")
process_log_file('candump-2024-07-18_013952.log.1', specified_can_id, 'filtered_can_messages.csv')
