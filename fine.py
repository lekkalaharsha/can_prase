import csv
import datetime
import cantools
import can

# Define the paths to your files
log_file_path = 'candump-2024-07-18_013952.log.1'
dbc_file_path = 'Zekrom_CANbus_1.dbc'
csv_file_path = 'filtered_can_messages.csv'

# Load the DBC file
db = cantools.database.load_file(dbc_file_path)

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

        # Convert data bytes to a byte array
        data_bytes = bytes.fromhex(data)

        # Decode the CAN message using the DBC file
        try:
            message_obj = db.get_message_by_frame_id(int(can_id, 16))
            decoded_data = message_obj.decode(data_bytes)
        except Exception as e:
            print(f"Error decoding CAN message with ID {can_id}: {e}")
            decoded_data = None

        return {
            "timestamp": human_readable_timestamp,
            "interface": interface,
            "can_id": can_id,
            "data_bytes": data,
            "decoded_data": decoded_data
        }
    except Exception as e:
        print(f"Error parsing line: {line.strip()} - {e}")
        return None

# Specify the CAN ID to filter
specified_can_id = input("Enter the CAN ID: ")

# Define the CSV header
csv_header = ['timestamp', 'interface', 'can_id', 'data_bytes', 'decoded_data']

# Open the log file and the CSV file
with open(log_file_path, 'r') as log_file, open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_header)
    writer.writeheader()
    
    # Process the log file line by line
    for line in log_file:
        if line.strip():
            parsed_message = parse_can_message(line)
            if parsed_message and parsed_message['can_id'] == specified_can_id:
                # Convert decoded_data to a string for CSV storage
                parsed_message['decoded_data'] = str(parsed_message['decoded_data'])
                writer.writerow(parsed_message)

print(f'CSV file "{csv_file_path}" with CAN ID {specified_can_id} has been created successfully.')
