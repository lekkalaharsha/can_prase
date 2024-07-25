import cantools
import can

# Load the DBC file
dbc_file = 'Zekrom_CANbus_1.dbc'
db = cantools.database.load_file(dbc_file)

# Open the CAN log file
log_file = 'candump-2024-07-22_091800.log'

with open(log_file, 'r') as f:
    for line in f:
        # Assuming the log format is: Time, ID, DLC, Data
        parts = line.strip().split()
        timestamp = parts[0]
        message_id = int(parts[1], 16)
        data_bytes = bytes.fromhex(''.join(parts[3:]))

        # Decode the CAN message using the DBC database
        try:
            message = db.get_message_by_frame_id(message_id)
            decoded_signals = message.decode(data_bytes)

            print(f"Timestamp: {timestamp}")
            print(f"Message ID: {message_id}")
            print(f"Signals: {decoded_signals}")

        except KeyError:
            print(f"Unknown Message ID: {message_id}")
