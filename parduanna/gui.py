import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def process_files():
    volume_csv = volume_entry.get()
    fid_csv = fid_entry.get()
    output_csv = output_entry.get()

    try:
        # Your existing code here, but replace print statements with messagebox.showinfo
        volume_df = pd.read_csv(volume_csv)
        fid_df = pd.read_csv(fid_csv)

        # ... (rest of your processing code)

        merged_df.to_csv(output_csv, index=False)
        messagebox.showinfo("Success", f"Resulting data saved to {output_csv}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

# Create the main window
root = tk.Tk()
root.title("CSV Processor")

# Create and pack widgets
tk.Label(root, text="Volume CSV:").pack()
volume_entry = tk.Entry(root, width=50)
volume_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(volume_entry)).pack()

tk.Label(root, text="FID CSV:").pack()
fid_entry = tk.Entry(root, width=50)
fid_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(fid_entry)).pack()

tk.Label(root, text="Output CSV:").pack()
output_entry = tk.Entry(root, width=50)
output_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(output_entry)).pack()

tk.Button(root, text="Process Files", command=process_files).pack()

root.mainloop()