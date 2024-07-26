import re
import datetime
import cantools
import csv
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' for non-interactive, or 'Qt5Agg'
import matplotlib.pyplot as plt


# Define the path to your DBC file
dbc_file_path = 'Zekrom_CANbus_1.dbc'

# Load the DBC file
db = cantools.database.load_file(dbc_file_path)

# Regular expression pattern for parsing CAN log lines
log_pattern = re.compile(r'\((\d+\.\d+)\) (\S+) (\S+)#(\S*)')

def parse_can_message(line, can_ids):
    """Parse a single CAN message line and return the decoded data if CAN ID matches."""
    match = log_pattern.match(line)
    if not match:
        return None

    timestamp_str, interface, can_id, data = match.groups()

    if can_id not in can_ids:
        return None

    timestamp = float(timestamp_str)
    human_readable_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

    data_bytes = bytes.fromhex(data)

    try:
        can_id_int = int(can_id, 16)
        message_obj = db.get_message_by_frame_id(can_id_int)
        
        expected_length = message_obj.length
        if len(data_bytes) != expected_length:
            print(f"Warning: Data length for CAN ID {can_id} is {len(data_bytes)}, but expected length is {expected_length}.")
            decoded_data = {}
        else:
            decoded_data = message_obj.decode(data_bytes) if message_obj else {}
    except KeyError:
        print(f"CAN ID {can_id} not found in the DBC file.")
        decoded_data = {}
    except ValueError as e:
        print(f"Error decoding CAN ID {can_id}: {e}")
        decoded_data = {}

    return {
        "timestamp": human_readable_timestamp,
        "interface": interface,
        "can_id": can_id,
        "data_bytes": data,
        **decoded_data  # Add decoded data to the result
    }

def process_log_file(log_file_path, can_ids, csv_file_path):
    """Process the log file and write the decoded data to a CSV file for the given CAN IDs."""
    parsed_messages = []
    signal_names = []

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if line.strip():
                parsed_message = parse_can_message(line, can_ids)
                if parsed_message:
                    parsed_messages.append(parsed_message)
                    # Add new signal names to the list in the order they appear
                    for key in parsed_message.keys():
                        if key not in signal_names and key not in ['timestamp', 'interface', 'can_id', 'data_bytes']:
                            signal_names.append(key)

    header = ['timestamp', 'interface', 'can_id', 'data_bytes'] + signal_names

    parsed_messages.sort(key=lambda x: datetime.datetime.strptime(x['timestamp'], '%Y-%m-%d %H:%M:%S.%f'))

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        for message in parsed_messages:
            row = {key: message.get(key, '') for key in header}
            writer.writerow(row)

    print(f'CSV file "{csv_file_path}" with specified CAN IDs has been created successfully.')

    return parsed_messages, signal_names

def plot_can_data(parsed_messages, signal_names, can_ids):
    """Plot CAN data for the specified CAN IDs."""
    # Organize data by CAN ID
    data_by_can_id = {can_id: {'timestamps': [], **{signal: [] for signal in signal_names}} for can_id in can_ids}

    for message in parsed_messages:
        if message['can_id'] in can_ids:
            timestamp = datetime.datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            data_by_can_id[message['can_id']]['timestamps'].append(timestamp)
            for signal in signal_names:
                if signal in message:
                    data_by_can_id[message['can_id']][signal].append(message[signal])

    plt.figure(figsize=(12, 6))
    for can_id, data in data_by_can_id.items():
        timestamps = data['timestamps']
        for signal, values in data.items():
            if signal != 'timestamps':
                # Ensure timestamps and values have the same length
                if len(timestamps) != len(values):
                    print(f"Warning: Length mismatch for CAN ID {can_id} - Signal {signal}. Timestamps: {len(timestamps)}, Values: {len(values)}")
                    # Optionally, trim data to the minimum length
                    min_length = min(len(timestamps), len(values))
                    timestamps = timestamps[:min_length]
                    values = values[:min_length]

                plt.plot(timestamps, values, label=f"CAN ID: {can_id} - {signal}")

    plt.title("CAN Data Plot", fontsize=16)
    plt.xlabel('Time')
    plt.ylabel('Signal Values')
    plt.legend()
    plt.grid(True)

    # Format the x-axis to show the time in a readable format
    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.gcf().autofmt_xdate()  # Rotate and align the tick labels
    
    plt.tight_layout()
    plt.savefig('plot.png')  # Save plot to a file
    print("Plot saved as 'plot.png'.")
    plt.show()

# Specify the CAN IDs to filter
can_ids_input = input("Enter the CAN IDs (comma-separated): ")
can_ids = set(can_ids_input.split(','))

# Process the log file for the given CAN IDs
csv_file_path = 'plot.csv'
parsed_messages, signal_names = process_log_file('candump-2024-07-18_013952.log.1', can_ids, csv_file_path)

# Plotting
plot_can_data(parsed_messages, signal_names, can_ids)
