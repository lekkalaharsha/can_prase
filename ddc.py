import canmatrix.formats

# Load the DBC file
dbc_file_path = 'Zekrom_CANbus_1.dbc'  # replace with your file path
matrix = canmatrix.formats.loadp(dbc_file_path)

# Assuming the 'loadp' function returns a dict, we'll access the first key-value pair
for name, db in matrix.items():
    # Iterate over frames (messages)
    for frame in db.frames:
        print(frame)
      
        # Iterate over signals in each message
        for signal in frame.signals:
            print(signal)
       
