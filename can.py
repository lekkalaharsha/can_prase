import datetime

# Sample CAN message
can_message = "(1721620080.711992) can0 6D0#28FFF503E4001EF9"

# Extract parts of the CAN message
timestamp_str, interface_data = can_message.split(") ")
timestamp = float(timestamp_str.strip("("))
interface, can_data = interface_data.split(" ")
can_id, data = can_data.split("#")

# Convert timestamp to a human-readable format
human_readable_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

# Split the data into bytes
data_bytes = [data[i:i+2] for i in range(0, len(data), 2)]

# Print the extracted information
print(f"Timestamp: {human_readable_timestamp}")
print(f"CAN Interface: {interface}")
print(f"CAN ID: {can_id}")
print("Data Bytes:")
for i, byte in enumerate(data_bytes):
    print(f"Byte {i+1}: {byte}")

# Optionally, you can convert data bytes to integers for further processing
data_integers = [int(byte, 16) for byte in data_bytes]
print("\nData Integers:")
print(data_integers)
