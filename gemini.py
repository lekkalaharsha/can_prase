import canmatrix
import  prashing
import csv
import datetime

def parse_can_data(dbc_file, can_file):
    """Parses CAN data based on a DBC file.

    Args:
        dbc_file (str): Path to the DBC file.
        can_file (str): Path to the CAN data file.
    """

    # Load the DBC file
    matrix = canmatrix.formats.loadp(dbc_file)

    # Open the CAN bus (replace 'can0' with your actual interface)
    bus = prashing.parse_can_message()


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
            "data_integers": data_integers
        }
    except Exception as e:
        print(f"Error parsing line: {line.strip()} - {e}")
        return None




    # Read CAN messages and process
    # with can.BufferedReader(bus) as reader:
    #     for msg in reader:
    #         # Find the corresponding message in the DBC
    #         try:
    #             dbc_msg = db.get_message_by_id(msg.arbitration_id)
    #             if dbc_msg:
    #                 # Decode the message and print signal values
    #                 decoded_msg = dbc_msg.decode(msg.data)
    #                 print(decoded_msg)
    #             else:
    #                 print(f"Unknown message ID: {msg.arbitration_id}")
    #         except cantools.database.errors.DatabaseError:
    #             print(f"Error decoding message: {msg}")

if __name__ == "__main__":
    dbc_file = "Zekrom_CANbus_1.dbc"
    can_file = "candump-2024-07-22_091800.log.1"
    parse_can_data(dbc_file, can_file)
